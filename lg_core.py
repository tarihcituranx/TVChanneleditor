"""
lg_core.py – LG GlobalClone XML (.tll) kanal listesi motoru
ChanSort GcXmlSerializer.cs kaynak kodundan tersine mühendislik ile Python'a çevrilmiştir.

Desteklenen format: LG TV'lerin GlobalClone XML formatındaki .tll dosyaları
  - Kök eleman: <TLLDATA>
  - Kanal listesi: <CHANNEL><ATV>...</ATV><DTV>...</DTV></CHANNEL>
  - Her kanal: <ITEM> elemanı içinde prNum, vchName, sourceIndex, isBlocked, isSkipped, isInvisable, frequency, serviceType vb.
"""

import xml.etree.ElementTree as ET
import re
import os


# --------------------------------------------------------------------------- #
#  serviceType → kanal tipi eşlemesi (LG DVB standartlarına göre)
# --------------------------------------------------------------------------- #
_SERVICE_TYPE_MAP = {
    1:  "TV",          # Digital TV
    2:  "Radio",       # Digital Radio
    4:  "NVoD",
    22: "AdvancedCodec",
    25: "HD TV",
    31: "HD AVC",
}

def _service_type_name(st: int) -> str:
    return _SERVICE_TYPE_MAP.get(st, f"Type{st}")


# --------------------------------------------------------------------------- #
#  XML yardımcı: geçersiz XML karakterlerini gör/gizle
# --------------------------------------------------------------------------- #
_INVALID_CHAR_RE = re.compile(r'&#x([0-9a-fA-F])([0-9a-fA-F]);')

def _replace_invalid_xml(text: str) -> str:
    out = []
    for c in text:
        code = ord(c)
        if (code < 0x20 and c not in ('\r', '\n', '\t')) or (0x7f <= code <= 0x9f):
            out.append(chr(0xE000 + code))
        else:
            out.append(c)
    return ''.join(out)

def _restore_invalid_xml(text: str) -> str:
    out = []
    for c in text:
        code = ord(c)
        if 0xE000 <= code <= 0xE09F:
            out.append(chr(code - 0xE000))
        else:
            out.append(c)
    return ''.join(out)



# --------------------------------------------------------------------------- #
#  LG eski format: "binary in UTF-8 envelope" isim çözümleme
# --------------------------------------------------------------------------- #
def _parse_lg_name(text: str) -> str:
    """
    Eski LG GlobalClone dosyalarında kanal ismi UTF-8 zarfı içinde binary veri olarak saklanır.
    ChanSort ParseName() metodunun Python karşılığı.
    Eğer ilk byte >= 0xC0 değilse düz string döndürür.
    """
    raw = text.encode('utf-8')
    if not raw or raw[0] < 0xC0:
        return text          # yeni format – düz metin

    out = bytearray()
    i = 0
    while i < len(raw):
        b0 = raw[i]
        if b0 >= 0xE0 and i + 2 < len(raw):       # 3-byte envelope → 2 input bytes
            b1, b2 = raw[i + 1], raw[i + 2]
            ch1 = ((b1 & 0x03) << 6) | (b2 & 0x3F)
            ch2 = ((b0 & 0x0F) << 4) | ((b1 & 0x3C) >> 2)
            out.append(ch1)
            out.append(ch2)
            i += 3
        elif b0 >= 0xC0 and i + 1 < len(raw):     # 2-byte envelope → 1 input byte
            b1 = raw[i + 1]
            out.append(((b0 & 0x03) << 6) | (b1 & 0x3F))
            i += 2
        else:                                       # 1-byte
            out.append(b0)
            i += 1

    try:
        # DVB charset: ilk byte encoding indicator olabilir (0x15 = UTF-8)
        if out and out[0] == 0x15:
            return bytes(out[1:]).decode('utf-8', errors='replace')
        return bytes(out).decode('latin-1', errors='replace')
    except Exception:
        return text


class LgEditor:
    """
    LG GlobalClone XML (.tll) kanal listesi okuyucu/yazıcı.

    Kullanım:
        ed = LgEditor('path/to/file.tll')
        ed.extract()
        channels = ed.get_channels()
        ed.update_channels(channels, 'output.tll')
        ed.cleanup()
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._root = None
        self._channels = []
        # <ITEM> node listesi – güncelleme için orijinal node'ları saklarız
        self._item_nodes = []

    # ----------------------------------------------------------------------- #
    def extract(self):
        """Dosyayı oku ve parse et."""
        with open(self.file_path, 'r', encoding='utf-8', errors='replace') as f:
            raw = f.read()

        if not raw.lstrip().startswith('<'):
            raise ValueError("Geçersiz LG GlobalClone dosyası: XML değil (binary .tll olabilir)")

        safe = _replace_invalid_xml(raw)
        try:
            self._root = ET.fromstring(safe)
        except ET.ParseError as e:
            raise ValueError(f"LG .tll XML parse hatası: {e}")

        if self._root.tag != 'TLLDATA':
            raise ValueError("Desteklenmeyen format: kök eleman <TLLDATA> değil")

        self._channels = []
        self._item_nodes = []
        self._parse_channels()

    # ----------------------------------------------------------------------- #
    def _parse_channels(self):
        """TLLDATA/CHANNEL/{ATV,DTV}/ITEM düğümlerini işle."""
        channel_node = self._root.find('CHANNEL')
        if channel_node is None:
            return

        uid = 0
        for list_node in channel_node:
            tag = list_node.tag
            if tag == 'ATV':
                analog = True
            elif tag == 'DTV':
                analog = False
            else:
                continue

            for item in list_node.findall('ITEM'):
                ch = self._parse_item(item, analog, uid)
                if ch is not None:
                    self._channels.append(ch)
                    self._item_nodes.append(item)
                    uid += 1

    # ----------------------------------------------------------------------- #
    def _parse_item(self, item, analog, uid):
        """Tek bir <ITEM> düğümünden kanal dict'i üret."""
        d = {
            'id':       uid,
            'num':      -1,
            'name':     '',
            'type':     'Analog' if analog else 'DTV',
            'freq':     0.0,
            'skip':     False,
            'lock':     False,
            'hide':     False,
            'fav1':     False,
            'fav2':     False,
            'fav3':     False,
            'fav4':     False,
            'fav5':     False,
            # extra
            'service_type': 0,
            'onid':     0,
            'tsid':     0,
            'sid':      0,
            'source':   'Antenna',
            'deleted':  False,
            'disabled': False,
        }

        map_type = 0
        has_hex_name = False

        for child in item:
            tag = child.tag
            txt = (child.text or '').strip()

            if tag == 'prNum':
                try:
                    num = int(txt)
                    if num != -1:
                        num &= 0x3FFF      # üst bitler (radio flag) temizle
                    d['num'] = num
                except ValueError:
                    pass

            elif tag == 'vchName':
                if not has_hex_name:
                    d['name'] = _parse_lg_name(txt) if txt else ''

            elif tag == 'hexVchName':
                try:
                    raw_bytes = bytes.fromhex(txt)
                    if raw_bytes and raw_bytes[0] == 0x15:
                        d['name'] = raw_bytes[1:].decode('utf-8', errors='replace')
                    else:
                        d['name'] = raw_bytes.decode('latin-1', errors='replace')
                    has_hex_name = True
                except Exception:
                    pass

            elif tag == 'sourceIndex':
                try:
                    src = int(txt)
                    if src == 2:
                        d['source'] = 'Cable'
                    elif src == 7:
                        d['source'] = 'Sat'
                    else:
                        d['source'] = 'Antenna'
                except ValueError:
                    pass

            elif tag == 'mapType':
                try:
                    map_type = int(txt)
                except ValueError:
                    pass

            elif tag == 'mapAttr':
                if map_type == 1:
                    try:
                        fav_int = int(txt)
                        d['fav1'] = bool(fav_int & 0x01)
                        d['fav2'] = bool(fav_int & 0x02)
                        d['fav3'] = bool(fav_int & 0x04)
                        d['fav4'] = bool(fav_int & 0x08)
                        d['fav5'] = bool(fav_int & 0x10)
                    except ValueError:
                        pass

            elif tag == 'isBlocked':
                d['lock'] = txt == '1'

            elif tag == 'isSkipped':
                d['skip'] = txt == '1'

            elif tag == 'isInvisable':   # LG'nin imla hatası
                d['hide'] = txt == '1'

            elif tag == 'isDeleted':
                d['deleted'] = txt != '0'

            elif tag == 'isDisabled':
                d['disabled'] = txt != '0'

            elif tag == 'serviceType':
                try:
                    st = int(txt)
                    d['service_type'] = st
                    d['type'] = _service_type_name(st)
                except ValueError:
                    pass

            elif tag == 'frequency':
                try:
                    freq_raw = int(txt)
                    if d['source'] == 'Sat':
                        d['freq'] = float(freq_raw)          # MHz (Sat)
                    else:
                        d['freq'] = freq_raw / 1000.0        # kHz → MHz
                except ValueError:
                    pass

            elif tag == 'pllData':       # ATV frekans
                try:
                    d['freq'] = int(txt) / 20.0
                except ValueError:
                    pass

            elif tag == 'original_network_id':
                try:
                    d['onid'] = int(txt)
                except ValueError:
                    pass

            elif tag == 'transport_id':
                try:
                    d['tsid'] = int(txt)
                except ValueError:
                    pass

            elif tag == 'service_id':
                try:
                    d['sid'] = int(txt)
                except ValueError:
                    pass

        return d

    # ----------------------------------------------------------------------- #
    def get_channels(self):
        """
        Kanal listesini döndürür.
        Her kanal: {id, num, name, type, freq, skip, lock, hide, fav1-5}
        """
        return list(self._channels)

    # ----------------------------------------------------------------------- #
    def update_channels(self, new_channels, output_path):
        """
        Güncellenen kanal listesini orijinal XML'e yaz ve output_path'e kaydet.

        new_channels: get_channels() çıktısıyla aynı yapı, num/name/skip/lock/hide/fav1-5 alanları güncellenir.
        """
        if self._root is None:
            raise RuntimeError("Önce extract() çağrılmalı")

        # id → new_channel eşlemesi
        update_map = {ch['id']: ch for ch in new_channels}

        for idx, item in enumerate(self._item_nodes):
            if idx not in update_map:
                continue
            upd = update_map[idx]

            # Favori bitmask hesapla
            fav_int = 0
            for bit, key in enumerate(['fav1', 'fav2', 'fav3', 'fav4', 'fav5']):
                if upd.get(key, False):
                    fav_int |= (1 << bit)

            map_type_val = None
            for child in item:
                tag = child.tag

                if tag == 'prNum':
                    num = upd.get('num', -1)
                    # Radio kanalları için 0x4000 biti korunur
                    orig_text = (child.text or '').strip()
                    try:
                        orig_num = int(orig_text)
                        radio_flag = orig_num & 0x4000
                    except ValueError:
                        radio_flag = 0
                    child.text = str(num | radio_flag) if num != -1 else str(num)

                elif tag == 'vchName':
                    child.text = upd.get('name', child.text) or ' '
                    if not child.text:
                        child.text = ' '

                elif tag == 'hexVchName':
                    name = upd.get('name', '')
                    name_bytes = name.encode('utf-8')
                    needs_enc = len(name_bytes) != len(name)
                    prefix = '15' if needs_enc else ''
                    child.text = prefix + name_bytes.hex()

                elif tag == 'isBlocked':
                    child.text = '1' if upd.get('lock', False) else '0'

                elif tag == 'isSkipped':
                    child.text = '1' if upd.get('skip', False) else '0'

                elif tag == 'isInvisable':
                    child.text = '1' if upd.get('hide', False) else '0'

                elif tag == 'mapType':
                    map_type_val = (child.text or '').strip()
                    try:
                        mt = int(map_type_val)
                        if upd.get('deleted', False):
                            mt |= 0x02
                        else:
                            mt &= ~0x02
                        child.text = str(mt)
                        map_type_val = str(mt)
                    except ValueError:
                        pass

                elif tag == 'mapAttr':
                    if map_type_val == '1':
                        child.text = str(fav_int)

                elif tag == 'isDeleted':
                    child.text = '1' if upd.get('deleted', False) else '0'

                elif tag == 'isDisabled':
                    child.text = '1' if upd.get('disabled', False) else '0'

                elif tag == 'isUserSelCHNo':
                    orig_num = self._channels[idx].get('num', -1)
                    new_num = upd.get('num', orig_num)
                    if new_num != orig_num:
                        child.text = '0' if upd.get('deleted', False) else '1'

        # XML'i string'e çevir, geçersiz karakterleri geri yükle
        xml_str = _restore_invalid_xml(ET.tostring(self._root, encoding='unicode', xml_declaration=False))

        # LG formatı: <?xml ...?> + boş satır + içerik
        output = '<?xml version="1.0" encoding="UTF-8"?>\r\n\r\n' + xml_str
        if not output.endswith('\r\n'):
            output += '\r\n'

        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            f.write(output)

    # ----------------------------------------------------------------------- #
    def cleanup(self):
        """Geçici kaynakları temizle (bu sınıfta gerek yok, interface uyumu için)."""
        pass

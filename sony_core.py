"""
sony_core.py – Sony sdb.xml kanal listesi motoru
ChanSort.Loader.Sony/Serializer.cs kaynak kodundan tersine mühendislik ile Python'a çevrilmiştir.

Desteklenen formatlar:
  - FormatVer: 1.0.0, 1.1.0, 1.2.0  → KDL model (Service + Programme tablosu)
  - FormateVer: 1.1.0 (e-format)     → Android firmware modeller (Service tablosu + ui4_nw_mask)

Kök eleman: <SdbRoot>
  <SdbXml>
    <FormatVer> veya <FormateVer>
    <SdbT>   DVB-T
    <SdbC>   DVB-C
    <SdbGs>  DVB-S (General)
    <SdbPs>  DVB-S (Preset)
    <SdbCis> DVB-S (CI)
  </SdbXml>
  <CheckSum>
"""

from defusedxml import ElementTree as ET
import struct
import os


# --------------------------------------------------------------------------- #
#  Desteklenen format versiyonları
# --------------------------------------------------------------------------- #
SUPPORTED_FORMATS = {'1.0.0', '1.1.0', '1.2.0', 'e1.1.0'}

# --------------------------------------------------------------------------- #
#  DVB servis tipi → kanal tipi adı
# --------------------------------------------------------------------------- #
_SVC_TYPE_MAP = {
    1:  'TV',
    2:  'Radio',
    22: 'AdvCodecSD',
    25: 'HD TV',
    26: 'AdvCodecSDT2',
    31: 'HD AVC',
}

def _svc_type_name(st: int) -> str:
    return _SVC_TYPE_MAP.get(st, f'Type{st}')


# --------------------------------------------------------------------------- #
#  e-format NwMask bitleri
# --------------------------------------------------------------------------- #
NW_VISIBLE         = 0x0008
NW_FAV_MASK        = 0x00F0
NW_FAV1            = 0x0010
NW_FAV2            = 0x0020
NW_FAV3            = 0x0040
NW_FAV4            = 0x0080
NW_NOT_DEL         = 0x0200
NW_RADIO           = 0x0400
NW_TV              = 0x2000


def _parse_fav_flags(nw_mask: int) -> dict:
    """NwMask'tan fav1-4 bitlerini çıkar."""
    fav = (nw_mask & NW_FAV_MASK) >> 4
    return {
        'fav1': bool(fav & 0x1),
        'fav2': bool(fav & 0x2),
        'fav3': bool(fav & 0x4),
        'fav4': bool(fav & 0x8),
        'fav5': False,
    }


# --------------------------------------------------------------------------- #
#  CRC-32 (Sony checksum)
# --------------------------------------------------------------------------- #
def _crc32_table():
    table = []
    for i in range(256):
        crc = i
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xEDB88320
            else:
                crc >>= 1
        table.append(crc)
    return table

_CRC32_TABLE = _crc32_table()

def _calc_crc32(data: bytes) -> int:
    crc = 0xFFFFFFFF
    for b in data:
        crc = (crc >> 8) ^ _CRC32_TABLE[(crc ^ b) & 0xFF]
    return (~crc) & 0xFFFFFFFF


def _calc_sony_checksum(xml_text: str, is_e_format: bool) -> int:
    """
    Sony checksum: CRC32 of the <SdbXml>...</SdbXml> section (LF-normalized).
    e-format includes trailing newline after </SdbXml>.
    """
    start = xml_text.find('<SdbXml>')
    end   = xml_text.find('</SdbXml>') + len('</SdbXml>')
    if is_e_format:
        end += 1   # include trailing \n
    section = xml_text[start:end].replace('\r\n', '\n')
    return _calc_crc32(section.encode('utf-8'))


# --------------------------------------------------------------------------- #
#  Sony XML "loop" tablosunu dict'e çevir
#  Her child'ın loop="N" attribute'u varsa, satır bazlı split yapılır.
# --------------------------------------------------------------------------- #
def _split_lines(parent_node):
    """
    Sony XML'deki loop-tablosunu {field_name: [val1, val2, ...]} formatına çevirir.
    ChanSort SplitLines() metodunun Python karşılığı.
    """
    result = {}
    if parent_node is None:
        return result
    for child in parent_node:
        if child.get('loop') is None:
            continue
        inner = child.text or ''
        # Baştaki ve sondaki newline'ı kaldır (ChanSort: Substring(1, len-2))
        if len(inner) >= 2:
            inner = inner[1:-1]
        lines = inner.split('\n')
        if len(lines) == 1 and lines[0] == '':
            result[child.tag] = []
        else:
            result[child.tag] = lines
    return result


class SonyEditor:
    """
    Sony sdb.xml kanal listesi okuyucu/yazıcı.

    Kullanım:
        ed = SonyEditor('path/to/sdb.xml')
        ed.extract()
        channels = ed.get_channels()
        ed.update_channels(channels, 'output/sdb.xml')
        ed.cleanup()
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._doc = None              # ET.Element (SdbRoot)
        self._raw_text = ''
        self._newline = '\n'
        self._format = ''
        self._is_e = False
        self._channels = []           # tüm kanallar
        # format-specific veriler (save için saklanır)
        self._sdb_sections = {}       # {'SdbT': {'node': ..., 'svc_data': {...}, 'prog_data': {...}}}

    # ----------------------------------------------------------------------- #
    def extract(self):
        """sdb.xml dosyasını oku ve parse et."""
        with open(self.file_path, 'rb') as f:
            raw_bytes = f.read()
        self._raw_text = raw_bytes.decode('utf-8', errors='replace')
        self._newline = '\r\n' if '\r\n' in self._raw_text else '\n'

        try:
            self._doc = ET.fromstring(self._raw_text)
        except ET.ParseError as e:
            raise ValueError(f"Sony sdb.xml parse hatası: {e}")

        if self._doc.tag != 'SdbRoot':
            raise ValueError("Desteklenmeyen format: kök eleman <SdbRoot> değil")

        sdb_xml = self._doc.find('SdbXml')
        if sdb_xml is None:
            raise ValueError("Sony sdb.xml: <SdbXml> elemanı bulunamadı")

        self._read_sdb_xml(sdb_xml)

    # ----------------------------------------------------------------------- #
    def _read_sdb_xml(self, node):
        """FormatVer'i tespit et ve her sdb bölümünü parse et."""
        fmt_node = node.find('FormatVer')
        if fmt_node is not None:
            self._format = fmt_node.text or ''
            self._is_e = False
        else:
            fmt_node = node.find('FormateVer')   # Android typo
            if fmt_node is not None:
                self._format = 'e' + (fmt_node.text or '')
                self._is_e = True
            else:
                raise ValueError("Sony sdb.xml: FormatVer/FormateVer bulunamadı")

        if self._format not in SUPPORTED_FORMATS:
            raise ValueError(f"Desteklenmeyen Sony format versiyonu: {self._format}")

        self._channels = []
        self._sdb_sections = {}

        uid_counter = [0]

        # SdbT, SdbC, SdbGs, SdbPs, SdbCis
        for child in node:
            tag_lower = child.tag.lower()
            if tag_lower == 'sdbt':
                self._read_sdb_section(child, 'DVB-T', uid_counter)
            elif tag_lower == 'sdbc':
                self._read_sdb_section(child, 'DVB-C', uid_counter)
            elif tag_lower == 'sdbgs':
                self._read_sdb_section(child, 'DVB-S', uid_counter)
            elif tag_lower == 'sdbps':
                self._read_sdb_section(child, 'DVB-S-Preset', uid_counter)
            elif tag_lower == 'sdbcis':
                self._read_sdb_section(child, 'DVB-S-CI', uid_counter)

    # ----------------------------------------------------------------------- #
    def _read_sdb_section(self, section_node, source_name: str, uid_counter: list):
        """Tek bir SdbT/SdbC/SdbGs/... bölümünü işle."""
        # Transponder frekans bilgisi için
        transponders = self._read_transponders(section_node)

        section_data = {
            'node': section_node,
            'source': source_name,
            'transponders': transponders,
        }

        if self._is_e:
            chs = self._read_services_e(section_node, source_name, transponders, uid_counter)
        else:
            chs = self._read_services_standard(section_node, source_name, transponders, uid_counter)

        section_data['channels_start'] = len(self._channels) - len(chs)
        section_data['channels_count'] = len(chs)
        self._sdb_sections[section_node.tag] = section_data

    # ----------------------------------------------------------------------- #
    def _read_transponders(self, section_node) -> dict:
        """
        Multiplex/Transponder bilgisini oku.
        Döndürür: {mux_id: {'freq': MHz, 'onid': ..., 'tsid': ...}}
        """
        mux_node = section_node.find('Multiplex')
        if mux_node is None:
            return {}

        mux_data = _split_lines(mux_node)
        transponders = {}

        id_field = 'MuxID' if self._is_e else 'MuxRowId'
        if id_field not in mux_data:
            return {}

        ids = mux_data[id_field]
        count = len(ids)

        # Frekans alanı
        freq_key = None
        for k in ('ui4_freq', 'SysFreq', 'Freq'):
            if k in mux_data:
                freq_key = k
                break

        rf_node = mux_node.find('RfParam')
        rf_data = _split_lines(rf_node) if rf_node is not None else {}

        for i in range(count):
            try:
                mux_id = int(ids[i])
            except (ValueError, IndexError):
                continue

            freq_mhz = 0.0
            onid = tsid = 0

            if self._is_e:
                if freq_key:
                    try:
                        raw_f = int(mux_data[freq_key][i])
                        # Sat: direkt MHz, diğerleri Hz → MHz
                        if 'DVB-S' in self._get_current_source_name(section_node):
                            freq_mhz = raw_f / 1000.0 if raw_f > 100000 else float(raw_f)
                        else:
                            freq_mhz = raw_f / 1000000.0
                    except (ValueError, IndexError):
                        pass
            else:
                if 'Freq' in rf_data:
                    try:
                        freq_mhz = int(rf_data['Freq'][i]) / 1000.0
                    except (ValueError, IndexError):
                        pass
                if 'Onid' in mux_data:
                    try:
                        onid = int(mux_data['Onid'][i])
                    except (ValueError, IndexError):
                        pass
                if 'Tsid' in mux_data:
                    try:
                        tsid = int(mux_data['Tsid'][i])
                    except (ValueError, IndexError):
                        pass

            transponders[mux_id] = {'freq': freq_mhz, 'onid': onid, 'tsid': tsid}

        return transponders

    def _get_current_source_name(self, section_node) -> str:
        tag = section_node.tag.lower()
        if tag in ['sdbgs', 'sdbps', 'sdbcis']:
            return 'DVB-S'
        elif tag == 'sdbc':
            return 'DVB-C'
        elif tag == 'sdbt':
            return 'DVB-T'
        
        # Fallback for unexpected tags
        if 'sdbc' in tag: return 'DVB-C'
        if 'sdbt' in tag: return 'DVB-T'
        if 'sdb' in tag and 's' in tag.replace('sdb', ''): return 'DVB-S'
        return 'DVB-T'

    # ----------------------------------------------------------------------- #
    def _read_services_standard(self, section_node, source_name, transponders, uid_counter) -> list:
        """
        FormatVer 1.x.x (KDL model): Service + Programme tablosundan kanalları oku.
        """
        svc_node = section_node.find('Service')
        prog_node = section_node.find('Programme')
        if svc_node is None:
            return []

        svc_data = _split_lines(svc_node)
        prog_data = _split_lines(prog_node) if prog_node is not None else {}

        if 'ServiceRowId' not in svc_data:
            return []

        channels = []
        row_map = {}   # rowId → channel dict

        for i in range(len(svc_data['ServiceRowId'])):
            uid = uid_counter[0]
            uid_counter[0] += 1

            try:
                row_id = int(svc_data['ServiceRowId'][i])
            except (ValueError, IndexError):
                row_id = i

            name = svc_data.get('Name', [''] * (i + 1))[i] if 'Name' in svc_data else ''
            svc_type = int(svc_data.get('Type', ['0'] * (i + 1))[i]) if 'Type' in svc_data else 0

            try:
                mux_id = int(svc_data.get('MuxRowId', ['0'] * (i + 1))[i])
            except (ValueError, IndexError):
                mux_id = 0

            transp = transponders.get(mux_id, {})

            try:
                onid = int(svc_data.get('Onid', ['0'] * (i + 1))[i])
            except (ValueError, IndexError):
                onid = transp.get('onid', 0)
            try:
                tsid = int(svc_data.get('Tsid', ['0'] * (i + 1))[i])
            except (ValueError, IndexError):
                tsid = transp.get('tsid', 0)
            try:
                sid = int(svc_data.get('Sid', ['0'] * (i + 1))[i])
            except (ValueError, IndexError):
                sid = 0

            try:
                att = int(svc_data.get('Attribute', ['0'] * (i + 1))[i])
            except (ValueError, IndexError):
                att = 0

            ch = {
                'id':           uid,
                '_row_id':      row_id,
                '_section':     section_node.tag,
                '_svc_index':   i,
                'num':          -1,
                'name':         name,
                'type':         _svc_type_name(svc_type),
                'service_type': svc_type,
                'freq':         transp.get('freq', 0.0),
                'onid':         onid,
                'tsid':         tsid,
                'sid':          sid,
                'source':       source_name,
                'skip':         False,
                'lock':         False,
                'hide':         False,
                'fav1':         False,
                'fav2':         False,
                'fav3':         False,
                'fav4':         False,
                'fav5':         False,
                'deleted':      True,
                'encrypted':    bool(att & 0x08),
                # Programme verisi (save için sakla)
                '_svc_data':    {k: v[i] for k, v in svc_data.items() if i < len(v)},
                '_prog_data':   None,
            }

            channels.append(ch)
            row_map[row_id] = ch

        # Programme: kanalları aktif yap ve num ata
        if 'ServiceRowId' in prog_data:
            for i in range(len(prog_data['ServiceRowId'])):
                try:
                    row_id = int(prog_data['ServiceRowId'][i])
                except (ValueError, IndexError):
                    continue
                ch = row_map.get(row_id)
                if ch is None:
                    continue
                ch['deleted'] = False
                try:
                    ch['num'] = int(prog_data['No'][i])
                except (ValueError, IndexError, KeyError):
                    pass
                try:
                    flag = int(prog_data.get('Flag', ['0'] * (i + 1))[i])
                    ch['fav1'] = bool(flag & 0x01)
                    ch['fav2'] = bool(flag & 0x02)
                    ch['fav3'] = bool(flag & 0x04)
                    ch['fav4'] = bool(flag & 0x08)
                except (ValueError, IndexError, KeyError):
                    pass
                ch['_prog_data'] = {k: v[i] for k, v in prog_data.items() if i < len(v)}

        self._channels.extend(channels)
        return channels

    # ----------------------------------------------------------------------- #
    def _read_services_e(self, section_node, source_name, transponders, uid_counter) -> list:
        """
        FormateVer 1.1.0 (Android / e-format): Service tablosu + NwMask.
        """
        svc_node = section_node.find('Service')
        if svc_node is None:
            return []

        svc_data = _split_lines(svc_node)
        dvb_node = svc_node.find('dvb_info')
        dvb_data = _split_lines(dvb_node) if dvb_node is not None else {}

        if 'ui2_svl_rec_id' not in svc_data:
            return []

        channels = []
        count = len(svc_data['ui2_svl_rec_id'])

        for i in range(count):
            uid = uid_counter[0]
            uid_counter[0] += 1

            try:
                rec_id = int(svc_data['ui2_svl_rec_id'][i])
            except (ValueError, IndexError):
                rec_id = i

            try:
                no_raw = int(svc_data.get('No', ['0'] * (i + 1))[i])
                prog_nr = (no_raw >> 18) & 0x3FFF
            except (ValueError, IndexError):
                prog_nr = -1

            try:
                nw_mask = int(svc_data.get('ui4_nw_mask', ['0'] * (i + 1))[i])
            except (ValueError, IndexError):
                nw_mask = 0

            is_deleted = (nw_mask & NW_NOT_DEL) == 0
            try:
                b_del = svc_data.get('b_deleted_by_user', ['0'] * (i + 1))[i]
                is_deleted = is_deleted or (b_del != '1')
            except (IndexError, KeyError):
                pass

            name = svc_data.get('Name', [''] * (i + 1))[i].replace('&amp;', '&') if 'Name' in svc_data else ''

            try:
                sid = int(svc_data.get('ui2_prog_id', ['0'] * (i + 1))[i])
            except (ValueError, IndexError):
                sid = 0

            try:
                mux_id = int(svc_data.get('MuxID', ['0'] * (i + 1))[i])
            except (ValueError, IndexError):
                mux_id = 0
            transp = transponders.get(mux_id, {})

            try:
                svc_type = int(dvb_data.get('ui1_sdt_service_type', ['0'] * (i + 1))[i])
            except (ValueError, IndexError):
                svc_type = 0

            if nw_mask & NW_TV:
                ch_type = 'TV'
            elif nw_mask & NW_RADIO:
                ch_type = 'Radio'
            else:
                ch_type = _svc_type_name(svc_type)

            favs = _parse_fav_flags(nw_mask)

            # aui1_custom_data: fav konumları (space-separated)
            try:
                fav_nums_str = svc_data.get('aui1_custom_data', [''] * (i + 1))[i]
                fav_nums = fav_nums_str.split(' ') if fav_nums_str else []
                # sadece pozitif değerler "fav aktif" demek
                if len(fav_nums) >= 1 and int(fav_nums[0]) > 0:
                    favs['fav1'] = True
                if len(fav_nums) >= 2 and int(fav_nums[1]) > 0:
                    favs['fav2'] = True
                if len(fav_nums) >= 3 and int(fav_nums[2]) > 0:
                    favs['fav3'] = True
                if len(fav_nums) >= 4 and int(fav_nums[3]) > 0:
                    favs['fav4'] = True
            except (ValueError, IndexError):
                pass

            ch = {
                'id':           uid,
                '_rec_id':      rec_id,
                '_section':     section_node.tag,
                '_svc_index':   i,
                'num':          prog_nr,
                'name':         name,
                'type':         ch_type,
                'service_type': svc_type,
                'freq':         transp.get('freq', 0.0),
                'onid':         transp.get('onid', 0),
                'tsid':         transp.get('tsid', 0),
                'sid':          sid,
                'source':       source_name,
                'skip':         False,
                'lock':         False,
                'hide':         (nw_mask & NW_VISIBLE) == 0,
                'deleted':      is_deleted,
                'encrypted':    False,
                '_nw_mask':     nw_mask,
                '_svc_data':    {k: v[i] for k, v in svc_data.items() if i < len(v)},
                **favs,
            }

            channels.append(ch)

        self._channels.extend(channels)
        return channels

    # ----------------------------------------------------------------------- #
    def get_channels(self) -> list:
        """
        Kanal listesini döndürür.
        Her kanal: {id, num, name, type, freq, skip, lock, hide, fav1-5}
        """
        return list(self._channels)

    # ----------------------------------------------------------------------- #
    def update_channels(self, new_channels: list, output_path: str):
        """
        Güncellenen kanal listesini orijinal XML ağacına yaz ve output_path'e kaydet.
        Sony checksum otomatik hesaplanır.
        """
        if self._doc is None:
            raise RuntimeError("Önce extract() çağrılmalı")

        # id → update eşlemesi
        update_map = {ch['id']: ch for ch in new_channels}

        sdb_xml = self._doc.find('SdbXml')
        if sdb_xml is None:
            raise RuntimeError("SdbXml düğümü bulunamadı")

        for ch in self._channels:
            uid = ch['id']
            if uid not in update_map:
                continue
            upd = update_map[uid]

            section_tag = ch.get('_section', '')
            section_node = sdb_xml.find(section_tag)
            if section_node is None:
                continue

            idx = ch.get('_svc_index', -1)
            if idx < 0:
                continue

            if self._is_e:
                self._update_service_e(section_node, idx, ch, upd)
            else:
                self._update_service_standard(section_node, idx, ch, upd)

        # XML'i string'e serialize et
        xml_str = ET.tostring(self._doc, encoding='unicode', xml_declaration=True)
        # Checksum güncelle
        crc = _calc_sony_checksum(xml_str, self._is_e)
        if self._is_e:
            hex_crc = format(crc, 'x')
        else:
            hex_crc = '0x' + format(crc, 'X')

        # CheckSum elementini güncelle
        cs_node = self._doc.find('CheckSum')
        if cs_node is not None:
            cs_node.text = hex_crc
            xml_str = ET.tostring(self._doc, encoding='unicode', xml_declaration=True)

        # Trailing newline
        if not xml_str.endswith('\n'):
            xml_str += '\n'

        os.makedirs(os.path.dirname(output_path), exist_ok=True) if os.path.dirname(output_path) else None
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            f.write(xml_str)

    # ----------------------------------------------------------------------- #
    def _update_service_standard(self, section_node, idx: int, original: dict, upd: dict):
        """KDL modeli: Service node'unda Name'i güncelle, Programme'de No ve Flag'i güncelle."""
        svc_node = section_node.find('Service')
        if svc_node is None:
            return

        for child in svc_node:
            if child.get('loop') is None:
                continue
            if child.tag == 'Name':
                lines = (child.text or '').split('\n')
                if idx + 1 < len(lines):
                    lines[idx + 1] = upd.get('name', original.get('name', ''))
                    child.text = '\n'.join(lines)

        prog_node = section_node.find('Programme')
        if prog_node is None:
            return

        for child in prog_node:
            if child.get('loop') is None:
                continue
            if child.tag == 'No':
                lines = (child.text or '').split('\n')
                if idx + 1 < len(lines):
                    lines[idx + 1] = str(upd.get('num', original.get('num', -1)))
                    child.text = '\n'.join(lines)
            elif child.tag == 'Flag':
                fav = 0
                if upd.get('fav1', False): fav |= 0x01
                if upd.get('fav2', False): fav |= 0x02
                if upd.get('fav3', False): fav |= 0x04
                if upd.get('fav4', False): fav |= 0x08
                lines = (child.text or '').split('\n')
                if idx + 1 < len(lines):
                    lines[idx + 1] = str(fav)
                    child.text = '\n'.join(lines)

    # ----------------------------------------------------------------------- #
    def _update_service_e(self, section_node, idx: int, original: dict, upd: dict):
        """Android e-format: Service node'unda ilgili alanları güncelle."""
        svc_node = section_node.find('Service')
        if svc_node is None:
            return

        new_nw_mask = original.get('_nw_mask', 0)
        # Favori bitleri
        new_nw_mask &= ~NW_FAV_MASK
        if upd.get('fav1', False): new_nw_mask |= NW_FAV1
        if upd.get('fav2', False): new_nw_mask |= NW_FAV2
        if upd.get('fav3', False): new_nw_mask |= NW_FAV3
        if upd.get('fav4', False): new_nw_mask |= NW_FAV4
        # Hidden
        if upd.get('hide', False):
            new_nw_mask &= ~NW_VISIBLE
        else:
            new_nw_mask |= NW_VISIBLE
        # Deleted
        if upd.get('deleted', False):
            new_nw_mask &= ~NW_NOT_DEL
        else:
            new_nw_mask |= NW_NOT_DEL

        for child in svc_node:
            if child.get('loop') is None:
                continue
            tag = child.tag
            lines = (child.text or '').split('\n')
            if idx + 1 >= len(lines):
                continue

            if tag == 'Name':
                lines[idx + 1] = upd.get('name', original.get('name', '')).replace('&', '&amp;')
                child.text = '\n'.join(lines)
            elif tag == 'ui4_nw_mask':
                lines[idx + 1] = str(new_nw_mask)
                child.text = '\n'.join(lines)
            elif tag == 'b_deleted_by_user':
                lines[idx + 1] = '0' if upd.get('deleted', False) else '1'
                child.text = '\n'.join(lines)
            elif tag == 'No':
                try:
                    old_no = int(lines[idx + 1])
                    new_num = upd.get('num', original.get('num', 0))
                    new_no = (new_num << 18) | (old_no & 0x3FFFF)
                    lines[idx + 1] = str(new_no)
                    child.text = '\n'.join(lines)
                except ValueError:
                    pass

    # ----------------------------------------------------------------------- #
    def cleanup(self):
        """Geçici kaynakları temizle (bu sınıfta gerek yok, interface uyumu için)."""
        pass

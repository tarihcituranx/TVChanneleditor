"""
hisense_core.py – Hisense servicelist.db / channel.db SQLite kanal listesi motoru
ChanSort.Loader.Hisense/ServicelistDb/ServicelistDbSerializer.cs kaynak kodundan
tersine mühendislik ile Python'a çevrilmiştir.

Desteklenen şemalar:
  - 2017 şeması: service, tuner, DVBCTuner/DVBSTuner/DVBTTuner, favoritelist, favoriteitem tabloları
  - 2021 şeması: service, tuner (tek tablo), servicelist, servicelistitem tabloları

Her iki şemada da DVB kanal listesi okunur/yazılır.
"""

import sqlite3
import shutil
import os


# --------------------------------------------------------------------------- #
#  Şema tespit ve sorgular
# --------------------------------------------------------------------------- #

class _Schema2017:
    """Hisense 2017 DB şeması (favoritelist / favoriteitem tabloları)."""
    channel_list_table   = 'favoritelist'
    dvb_service_table    = 'DVBService'
    short_name_field     = 's.ShortName'
    parental_lock_field  = 'digs.ParentalLock'
    select_channels      = """
        SELECT fi.FavoriteId, fi.ServiceId, fi.Number, fi.Selectable, fi.Visible,
               fi.Deleted, fi.Protected, fi.LCN
        FROM favoriteitem fi
    """
    update_service       = """
        UPDATE service SET
            Name=?, ShortName=?, ParentalLock=?, Visible=?, Selectable=?,
            Fav1=?, Fav2=?, Fav3=?, Fav4=?
        WHERE Pid=?
    """
    update_channel_item  = """
        UPDATE favoriteitem SET
            Number=?, Deleted=?, Protected=?, Selectable=?, Visible=?
        WHERE FavoriteId=? AND ServiceId=?
    """
    delete_fav_items     = "DELETE FROM favoriteitem WHERE FavoriteId IN (SELECT Pid FROM favoritelist WHERE Name LIKE 'FAV%')"
    insert_fav_item      = "INSERT INTO favoriteitem (FavoriteId, ServiceId, Number) VALUES (?, ?, ?)"


class _Schema2021:
    """Hisense 2021 DB şeması (servicelist / servicelistitem tabloları)."""
    channel_list_table   = 'servicelist'
    dvb_service_table    = 'DvbService'
    short_name_field     = 'digs.ShortName'
    parental_lock_field  = 'digs.Service11'
    select_channels      = """
        SELECT sli.ServiceListId, sli.ServiceId, sli.No, sli.Selectable, sli.Visible,
               sli.Deleted, sli.Protected, sli.LCN
        FROM servicelistitem sli
    """
    update_service       = """
        UPDATE service SET
            Name=?, ShortName=?, ParentalLock=?, Visible=?, Selectable=?,
            Fav1=?, Fav2=?, Fav3=?, Fav4=?
        WHERE Pid=?
    """
    update_channel_item  = """
        UPDATE servicelistitem SET
            No=?, Deleted=?, Protected=?, Selectable=?, Visible=?
        WHERE ServiceListId=? AND ServiceId=?
    """
    delete_fav_items     = "DELETE FROM servicelistitem WHERE ServiceListId IN (SELECT Pid FROM servicelist WHERE Name LIKE 'FAV%')"
    insert_fav_item      = "INSERT INTO servicelistitem (ServiceListId, ServiceId, No) VALUES (?, ?, ?)"


# --------------------------------------------------------------------------- #
#  Frontend (tuner tipi) → kaynak adı
# --------------------------------------------------------------------------- #
_FRONTEND_MAP = {
    2: ('DVB-T',  'TV'),
    3: ('DVB-C',  'TV'),
    4: ('DVB-S',  'TV'),
    6: ('DVB-T2', 'TV'),
}


class HisenseEditor:
    """
    Hisense servicelist.db / channel.db SQLite kanal listesi okuyucu/yazıcı.

    Kullanım:
        ed = HisenseEditor('path/to/servicelist.db')
        ed.extract()
        channels = ed.get_channels()
        ed.update_channels(channels, 'output.db')
        ed.cleanup()
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._schema = None
        self._channels = []          # [{id, num, name, ...}, ...]
        # Kaydetme için ek veriler
        self._channels_by_id = {}    # service_pid → channel dict
        self._list_map = {}          # list_pid → list_name
        self._fav_lists = {}         # list_pid → fav_index (0-3)
        self._pid_all = 0
        self._pid_av  = 0
        # Transponder/tuner verileri
        self._transponders = {}      # tuner_id → {freq_mhz, onid, tsid, source}

    # ----------------------------------------------------------------------- #
    def extract(self):
        """SQLite dosyasını oku ve parse et."""
        try:
            conn = sqlite3.connect(self.file_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
        except Exception as e:
            raise ValueError(f"SQLite bağlantı hatası: {e}")

        try:
            # Tablo listesini al
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            table_names = {row[0].lower() for row in cur.fetchall()}

            # Şema tespiti
            if 'favoritelist' in table_names:
                self._schema = _Schema2017()
            elif 'servicelist' in table_names:
                self._schema = _Schema2021()
            else:
                raise ValueError("Hisense DB: desteklenen tablo yapısı bulunamadı (favoritelist veya servicelist gerekli)")

            if 'service' not in table_names or 'tuner' not in table_names:
                raise ValueError("Hisense DB: 'service' veya 'tuner' tablosu bulunamadı")

            # REINDEX – bozuk index'leri onar
            try:
                cur.execute("REINDEX")
            except Exception:
                pass

            self._load_lists(cur)
            self._load_transponders(cur, table_names)
            self._load_services(cur)
            self._load_channels(cur)

        finally:
            conn.close()

    # ----------------------------------------------------------------------- #
    def _load_lists(self, cur):
        """Kanal listesi adlarını ve FAV eşlemelerini yükle."""
        self._list_map = {}
        self._fav_lists = {}
        self._pid_all = 0
        self._pid_av  = 0

        try:
            cur.execute(f"SELECT Pid, Name FROM {self._schema.channel_list_table}")
        except Exception:
            return

        for row in cur.fetchall():
            pid  = row[0]
            name = row[1]
            self._list_map[pid] = name
            if name == '$all':
                self._pid_all = pid
            elif name == '$av':
                self._pid_av = pid
            elif name.startswith('FAV'):
                try:
                    fav_idx = int(name[3:]) - 1   # FAV1 → 0, FAV2 → 1 ...
                    self._fav_lists[pid] = fav_idx
                except ValueError:
                    pass

    # ----------------------------------------------------------------------- #
    def _load_transponders(self, cur, table_names: set):
        """Tuner tablosundan transponder bilgisi yükle."""
        self._transponders = {}

        # 2021 şeması: birleşik tuner tablosu (frontend sütunu ile)
        if 'frontend' in self._get_columns(cur, 'tuner'):
            try:
                cur.execute("SELECT tunerid, oid, tid, satellite, frequency, sr, frontend FROM tuner")
                for row in cur.fetchall():
                    tid, oid, tsid, sat, freq_hz, sr, fe = row
                    source, _ = _FRONTEND_MAP.get(fe, ('DVB-?', 'TV'))
                    self._transponders[tid] = {
                        'onid':     oid,
                        'tsid':     tsid,
                        'freq_mhz': freq_hz / 1000.0,
                        'source':   source,
                        'sat':      sat,
                    }
            except Exception:
                pass
            return

        # 2017 şeması: ayrı DVBCTuner / DVBSTuner / DVBTTuner tabloları
        type_tables = [
            ('dvbctuner',  'DVB-C',  'Frequency', 'symbolrate'),
            ('dvbctuner',  'DVB-C2', 'Frequency', 'bandwidth'),
            ('dvbstuner',  'DVB-S',  'Frequency', 'symbolrate'),
            ('dvbstuner',  'DVB-S2', 'Frequency', 'symbolrate'),
            ('dvbttuner',  'DVB-T',  'Frequency', 'bandwidth'),
            ('dvbttuner',  'DVB-T2', 'Frequency', 'bandwidth'),
        ]
        for table, source, freq_col, _ in type_tables:
            if table not in table_names:
                continue
            try:
                cur.execute(f"""
                    SELECT tuner.tunerid, oid, tid, satellite, {freq_col}
                    FROM tuner
                    INNER JOIN {table} ON {table}.tunerid = tuner.tunerid
                """)
                for row in cur.fetchall():
                    tid, oid, tsid, sat, freq_raw = row
                    self._transponders[tid] = {
                        'onid':     oid,
                        'tsid':     tsid,
                        'freq_mhz': freq_raw / 1000.0,
                        'source':   source,
                        'sat':      sat,
                    }
            except Exception:
                pass

    def _get_columns(self, cur, table: str) -> set:
        try:
            cur.execute(f"PRAGMA table_info({table})")
            return {row[1].lower() for row in cur.fetchall()}
        except Exception:
            return set()

    # ----------------------------------------------------------------------- #
    def _load_services(self, cur):
        """Service tablosundan kanal bilgilerini yükle (DVB + Analog)."""
        self._channels_by_id = {}

        short_name_field  = self._schema.short_name_field
        parental_lock_field = self._schema.parental_lock_field
        dvb_table         = self._schema.dvb_service_table

        try:
            cur.execute(f"""
                SELECT s.Pid, s.type,
                       anls.Frequency,
                       digs.TunerId, digs.Sid,
                       s.Name,
                       {short_name_field},
                       digs.Encrypted,
                       s.Visible, s.Selectable,
                       {parental_lock_field},
                       digs.MediaType
                FROM service s
                LEFT OUTER JOIN AnalogService anls ON anls.ServiceId = s.Pid
                LEFT OUTER JOIN {dvb_table} digs   ON digs.ServiceId = s.Pid
            """)
        except Exception as e:
            raise ValueError(f"Hisense DB: service sorgusu başarısız: {e}")

        for row in cur.fetchall():
            pid, svc_type, ana_freq, tuner_id, sid, name, short_name, enc, visible, sel, lock, media_type = row

            if ana_freq is not None:
                # Analog kanal
                ch = {
                    '_pid':     pid,
                    'id':       pid,
                    'num':      -1,
                    'name':     name or '',
                    'type':     'Analog',
                    'freq':     (ana_freq or 0) / 1000.0,
                    'onid':     0,
                    'tsid':     0,
                    'sid':      0,
                    'source':   'Analog',
                    'skip':     (sel or 1) == 0,
                    'lock':     bool(lock),
                    'hide':     (visible or 1) == 0,
                    'fav1':     False, 'fav2': False, 'fav3': False, 'fav4': False, 'fav5': False,
                    'deleted':  False,
                    'encrypted': False,
                    '_short':   '',
                    '_list':    '',
                }
                self._channels_by_id[pid] = ch

            elif tuner_id is not None:
                # DVB kanal
                transp = self._transponders.get(tuner_id, {})
                if media_type == 1:
                    ch_type = 'TV'
                elif media_type == 2:
                    ch_type = 'Radio'
                else:
                    ch_type = f'Type{media_type}'

                ch = {
                    '_pid':     pid,
                    '_tuner':   tuner_id,
                    'id':       pid,
                    'num':      -1,
                    'name':     name or '',
                    'type':     ch_type,
                    'freq':     transp.get('freq_mhz', 0.0),
                    'onid':     transp.get('onid', 0),
                    'tsid':     transp.get('tsid', 0),
                    'sid':      sid or 0,
                    'source':   transp.get('source', 'DVB'),
                    'skip':     (sel or 1) == 0,
                    'lock':     bool(lock),
                    'hide':     (visible or 1) == 0,
                    'fav1':     False, 'fav2': False, 'fav3': False, 'fav4': False, 'fav5': False,
                    'deleted':  False,
                    'encrypted': bool(enc),
                    '_short':   short_name or '',
                    '_list':    '',
                }
                self._channels_by_id[pid] = ch

    # ----------------------------------------------------------------------- #
    def _load_channels(self, cur):
        """FavoriteItem/ServiceListItem tablosundan program numaralarını yükle."""
        self._channels = []

        try:
            cur.execute(self._schema.select_channels)
        except Exception as e:
            raise ValueError(f"Hisense DB: kanal sorgusu başarısız: {e}")

        seen = set()

        for row in cur.fetchall():
            list_pid, srv_pid, number, sel, vis, deleted, prot, lcn = row

            ci = self._channels_by_id.get(srv_pid)
            if ci is None:
                continue

            fav_idx = self._fav_lists.get(list_pid, -1)

            if fav_idx >= 0:
                # FAV listesi – fav biti set et
                fav_key = f'fav{fav_idx + 1}'
                if fav_key in ci and (number or 0) > 0:
                    ci[fav_key] = True
                continue

            # Fiziksel liste
            list_name = self._list_map.get(list_pid, '')
            if list_name in ('$all', '$av'):
                # $all ve $av listelerindeki skip/lock/hide override'larını uygula
                if sel is not None and sel == 0:
                    ci['skip'] = True
                if prot is not None and prot == 1:
                    ci['lock'] = True
                if vis is not None and vis == 0:
                    ci['hide'] = True
                continue

            ci['num']     = number or -1
            ci['deleted'] = bool(deleted)
            ci['_list']   = list_name

            if sel is not None and sel == 0:
                ci['skip'] = True
            if prot is not None and prot == 1:
                ci['lock'] = True
            if vis is not None and vis == 0:
                ci['hide'] = True

            if srv_pid not in seen:
                seen.add(srv_pid)
                self._channels.append(ci)

        # Sırala
        self._channels.sort(key=lambda c: (c['num'] if c['num'] > 0 else 99999))

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
        Güncellenen kanal listesini output_path'e kaydet.
        Önce orijinal dosya kopyalanır, ardından SQLite üzerinde UPDATE yapılır.
        """
        # Dosyayı kopyala
        shutil.copy2(self.file_path, output_path)

        # id → update eşlemesi
        update_map = {ch['id']: ch for ch in new_channels}

        conn = sqlite3.connect(output_path)
        cur  = conn.cursor()

        try:
            cur.execute("BEGIN")

            schema = self._schema

            # 1) Service tablosunu güncelle (isim, skip, lock, hide, fav)
            for pid, ci in self._channels_by_id.items():
                upd = update_map.get(pid, ci)
                cur.execute(schema.update_service, (
                    upd.get('name',  ci.get('name', '')),
                    ci.get('_short', ''),
                    1 if upd.get('lock', False) else 0,
                    0 if upd.get('hide', False) else 1,
                    0 if upd.get('skip', False) else 1,
                    1 if upd.get('fav1', False) else 0,
                    1 if upd.get('fav2', False) else 0,
                    1 if upd.get('fav3', False) else 0,
                    1 if upd.get('fav4', False) else 0,
                    pid,
                ))

            # 2) Fiziksel kanal listesini güncelle (program numaraları)
            for ch in self._channels:
                pid = ch['_pid']
                upd = update_map.get(pid, ch)

                # list_pid'i bul
                list_name = ch.get('_list', '')
                list_pid  = None
                for lp, ln in self._list_map.items():
                    if ln == list_name:
                        list_pid = lp
                        break

                if list_pid is None:
                    continue

                cur.execute(schema.update_channel_item, (
                    upd.get('num', -1),
                    1 if upd.get('deleted', False) else 0,
                    1 if upd.get('lock', False) else 0,
                    0 if upd.get('skip', False) else -1,
                    0 if upd.get('hide', False) else -1,
                    list_pid,
                    pid,
                ))

                # $all listesini de güncelle
                if self._pid_all:
                    cur.execute(schema.update_channel_item, (
                        upd.get('num', -1),
                        1 if upd.get('deleted', False) else 0,
                        1 if upd.get('lock', False) else 0,
                        0 if upd.get('skip', False) else -1,
                        0 if upd.get('hide', False) else -1,
                        self._pid_all,
                        pid,
                    ))

            # 3) FAV listelerini güncelle (sil + tekrar ekle)
            cur.execute(schema.delete_fav_items)

            for fav_pid, fav_idx in self._fav_lists.items():
                fav_key = f'fav{fav_idx + 1}'
                fav_nr  = 1
                for ch in self._channels:
                    pid = ch['_pid']
                    upd = update_map.get(pid, ch)
                    if upd.get(fav_key, False):
                        cur.execute(schema.insert_fav_item, (fav_pid, pid, fav_nr))
                        fav_nr += 1

            conn.commit()

        except Exception as e:
            conn.rollback()
            conn.close()
            raise RuntimeError(f"Hisense DB güncelleme hatası: {e}")

        conn.close()

    # ----------------------------------------------------------------------- #
    def cleanup(self):
        """Geçici kaynakları temizle (bu sınıfta gerek yok, interface uyumu için)."""
        pass

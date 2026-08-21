import sqlite3
import zipfile
import tempfile
import os
import shutil

class TizenEditor:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.temp_dir = tempfile.mkdtemp()
        self.db_files = []
        self.channel_db_path = None
        self.encoding = 'utf-16-be' # default

    def extract(self):
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            for info in zip_ref.infolist():
                # Path traversal korumasi
                if info.filename.startswith('/') or '..' in info.filename:
                    continue
                zip_ref.extract(info, self.temp_dir)
        
        # Detect database files
        for f in os.listdir(self.temp_dir):
            path = os.path.join(self.temp_dir, f)
            if os.path.isfile(path) and not f.startswith('vconf_') and not f.endswith('-shm') and not f.endswith('-wal'):
                try:
                    conn = sqlite3.connect(path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = [row[0].upper() for row in cursor.fetchall()]
                    conn.close()
                    
                    if 'CHNL' in tables and 'SRV' in tables and 'SRV_DVB' in tables:
                        self.channel_db_path = path
                except:
                    pass

        if not self.channel_db_path:
            raise Exception("No supported Tizen DVB database found in the zip file.")

    def _decode_name(self, name_bytes):
        if not name_bytes:
            return ""
        
        # Auto-detect endianness
        even_zeros = 0
        odd_zeros = 0
        for i in range(0, len(name_bytes) - 1, 2):
            if name_bytes[i] == 0:
                even_zeros += 1
            if name_bytes[i+1] == 0:
                odd_zeros += 1
                
        enc = 'utf-16-be' if even_zeros >= odd_zeros else 'utf-16-le'
        try:
            return name_bytes.decode(enc).replace('\x00', '')
        except:
            return ""

    def _encode_name(self, name_str):
        if not name_str:
            return b''
        return name_str.encode(self.encoding)

    def get_channels(self):
        if not self.channel_db_path:
            return []

        conn = sqlite3.connect(self.channel_db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # We need to get channels and their fav status
        # In Tizen, major = PrNr. lockMode, hidden, numSel(!skip)
        # We will map it to our format
        query = """
            SELECT SRV.srvId, SRV.major as progNum, cast(SRV.srvName as blob) as srvNameBytes, 
                   SRV.hidden, SRV.lockMode, SRV.numSel, SRV.elim,
                   CHNL.freq, SRV_DVB.onid, SRV_DVB.tsid, SRV_DVB.vidPid, SRV_DVB.provId
            FROM SRV_DVB
            INNER JOIN SRV ON SRV.srvId = SRV_DVB.srvId
            INNER JOIN CHNL ON CHNL.chId = SRV.chId
            ORDER BY SRV.major ASC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Fetch favs
        cursor.execute("SELECT srvId, fav, pos FROM SRV_FAV")
        fav_rows = cursor.fetchall()
        fav_map = {}
        for r in fav_rows:
            sid = r['srvId']
            if sid not in fav_map:
                fav_map[sid] = []
            fav_map[sid].append(r['fav'])

        channels = []
        for r in rows:
            if r['elim'] != 0:
                continue
            
            srv_id = r['srvId']
            name_bytes = r['srvNameBytes']
            name = self._decode_name(name_bytes)
            
            # Map Tizen flags to our flags
            # numSel == 1 means selected (not skipped). numSel == 0 means skipped.
            # lockMode == 1 means locked.
            # hidden == 1 means hidden.
            is_skipped = (r['numSel'] == 0)
            is_locked = (r['lockMode'] != 0)
            is_hidden = (r['hidden'] != 0)
            
            fav_list = fav_map.get(srv_id, [])
            fav_flags = [False]*5
            for fav_idx in fav_list:
                if 1 <= fav_idx <= 5:
                    fav_flags[fav_idx - 1] = True
            
            # In Tizen, freq is usually in Hz or kHz. 
            freq_mhz = r['freq'] // 1000 if r['freq'] > 100000 else r['freq']

            ch = {
                'id': srv_id,  # We use srvId as the unique identifier
                'num': r['progNum'],
                'name': name,
                'type': 'TV' if r['vidPid'] != 0 else 'Radio', 'type_known': False,
                'freq': freq_mhz,
                'skip': is_skipped,
                'lock': is_locked,
                'hide': is_hidden,
                'encrypted': None, 'encrypted_known': False,
                'fav1': fav_flags[0],
                'fav2': fav_flags[1],
                'fav3': fav_flags[2],
                'fav4': fav_flags[3],
                'fav5': fav_flags[4],
                'sid': srv_id,
                'tsid': r['tsid'],
                'onid': r['onid'],
                'vidpid': r['vidPid'],
                'pcrpid': r['vidPid'], 'pcrpid_known': False
            }
            channels.append(ch)
            
        conn.close()
        return channels

    def update_channels(self, new_channels, output_zip_path):
        if not self.channel_db_path:
            raise Exception("Database not loaded.")

        conn = sqlite3.connect(self.channel_db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("BEGIN TRANSACTION")
            
            for ch in new_channels:
                srv_id = ch['id']
                progNum = ch['num']
                lockMode = 1 if ch.get('lock') else 0
                hidden = 1 if ch.get('hide') else 0
                numSel = 0 if ch.get('skip') else 1
                
                # Check if name was edited
                name_bytes = ch.get('name', '').encode('utf-16le')
                # Tizen stores it as a blob. We will update srvName.
                cursor.execute("""
                    UPDATE SRV SET 
                        major = ?, 
                        lockMode = ?, 
                        hidden = ?, 
                        hideGuide = ?, 
                        numSel = ?,
                        srvName = ?
                    WHERE srvId = ?
                """, (progNum, lockMode, hidden, hidden, numSel, name_bytes, srv_id))
                
                # Update Favs (Only Fav1 for now, or all 5 if provided)
                # First delete existing favs for this srvId
                cursor.execute("DELETE FROM SRV_FAV WHERE srvId = ?", (srv_id,))
                
                # Add new favs
                favs = [ch.get(f'fav{i}', False) for i in range(1, 6)]
                for i, is_fav in enumerate(favs):
                    if is_fav:
                        fav_id = i + 1
                        # In Tizen, pos is usually ordering inside fav list. We just put a sequential or 0.
                        cursor.execute("INSERT INTO SRV_FAV (srvId, fav, pos) VALUES (?, ?, ?)", (srv_id, fav_id, progNum))
                        
            cursor.execute("COMMIT")
            
            # Reindex to prevent corruption issues on Samsung TV
            cursor.execute("REINDEX")
            
        except Exception as e:
            cursor.execute("ROLLBACK")
            conn.close()
            raise e
            
        conn.close()
        
        # Create the new zip file
        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(self.temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.temp_dir)
                    zf.write(file_path, arcname)

    def cleanup(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

#!/usr/bin/env python3
import sys
import struct
import zipfile
import csv
import os

def parse_transponders(z, filename):
    tp_dict = {}
    if filename not in z.namelist():
        return tp_dict
    
    data = z.read(filename)
    # 4 bytes header, then 45 bytes per record
    for i in range(4, len(data), 45):
        rec = data[i:i+45]
        if len(rec) < 45:
            break
        tp_index = struct.unpack('<I', rec[1:5])[0]
        freq = struct.unpack('<I', rec[9:13])[0]
        sym = struct.unpack('<I', rec[13:17])[0]
        pol = rec[17]
        tp_dict[tp_index] = {
            'freq': freq // 1000,
            'sym': sym // 1000,
            'pol': 'V' if pol == 1 else 'H'
        }
    return tp_dict

def extract_to_csv(scm_path, csv_path):
    print(f"[*] Dosya okunuyor: {scm_path}")
    try:
        with zipfile.ZipFile(scm_path, 'r') as z:
            # Frekansları oku
            tp_dict = parse_transponders(z, 'TransponderDataBase.dat')
            tp_dict.update(parse_transponders(z, 'UserTransponderDataBase.dat'))
            
            # Kanalları oku
            sd = z.read('map-SateD')
    except Exception as e:
        print(f"[!] Hata: {e}")
        return

    channels = []
    # Her kayıt 168 byte
    for i in range(0, len(sd), 168):
        rec = sd[i:i+168]
        if len(rec) < 168:
            break
        
        # Boş slot kontrolü (hepsi 0 ise)
        if all(b == 0 for b in rec):
            continue

        channelNo = struct.unpack('<H', rec[0:2])[0]
        serviceType_byte = rec[14]
        if serviceType_byte in (25, 0x11, 0x19):
            sType = "HD"
        elif serviceType_byte == 2:
            sType = "Radio"
        else:
            sType = "SD"
            
        name_bytes = rec[36:36+96]
        name = name_bytes.decode('utf-16be', errors='ignore').split('\0')[0]
        
        encrypted = "Yes" if rec[136] == 1 else "No"
        tp_index = struct.unpack('<H', rec[18:20])[0]
        
        freq_info = tp_dict.get(tp_index, {'freq': '???', 'sym': '???', 'pol': '?'})
        
        channels.append({
            'Slot': i // 168,
            'No': channelNo,
            'Name': name,
            'Type': sType,
            'Encrypted': encrypted,
            'Freq': freq_info['freq'],
            'Pol': freq_info['pol'],
            'Sym': freq_info['sym']
        })
    
    print(f"[*] {len(channels)} aktif kanal bulundu. CSV'ye aktarılıyor...")
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Slot', 'No', 'Name', 'Type', 'Encrypted', 'Freq', 'Pol', 'Sym'])
        writer.writeheader()
        channels.sort(key=lambda x: x['No'])
        for c in channels:
            writer.writerow(c)
    
    print(f"[+] Başarılı! Kanallar '{csv_path}' dosyasına kaydedildi.")

def build_from_csv(original_scm, csv_path, new_scm):
    print(f"[*] CSV dosyası okunuyor: {csv_path}")
    edited_channels = {}
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                slot = int(row['Slot'])
                edited_channels[slot] = {
                    'No': int(row['No']),
                    'Name': row['Name']
                }
    except Exception as e:
        print(f"[!] CSV Okuma Hatası: {e}")
        return

    print(f"[*] Orijinal SCM açılıyor ve yeni liste oluşturuluyor: {new_scm}")
    try:
        with zipfile.ZipFile(original_scm, 'r') as zin:
            with zipfile.ZipFile(new_scm, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    data = zin.read(item.filename)
                    
                    if item.filename == 'map-SateD':
                        out_data = bytearray()
                        active_records = []
                        for i in range(0, len(data), 168):
                            rec = bytearray(data[i:i+168])
                            if len(rec) < 168:
                                break
                                
                            slot = i // 168
                            if slot in edited_channels:
                                edits = edited_channels[slot]
                                
                                struct.pack_into('<H', rec, 0, edits['No'])
                                
                                name_bytes = edits['Name'].encode('utf-16be')[:94]
                                for j in range(96):
                                    rec[36+j] = 0
                                rec[36:36+len(name_bytes)] = name_bytes
                                
                                active_records.append(rec)
                                
                        for rec in active_records:
                            csum = sum(rec[:167]) % 256
                            rec[167] = csum
                            out_data.extend(rec)
                            
                        padding_len = len(data) - len(out_data)
                        if padding_len > 0:
                            out_data.extend(b'\x00' * padding_len)
                            
                        zout.writestr(item, out_data)
                    else:
                        zout.writestr(item, data)
                        
    except Exception as e:
        print(f"[!] Hata: {e}")
        return

    print(f"[+] İşlem tamam! Yeni dosyanız hazır: {new_scm}")

def get_channels(scm_path):
    try:
        with zipfile.ZipFile(scm_path, 'r') as z:
            tp_dict = parse_transponders(z, 'TransponderDataBase.dat')
            tp_dict.update(parse_transponders(z, 'UserTransponderDataBase.dat'))
            sd = z.read('map-SateD')
    except Exception as e:
        return []
    channels = []
    for i in range(0, len(sd), 168):
        rec = sd[i:i+168]
        if len(rec) < 168: break
        if all(b == 0 for b in rec): continue
        channelNo = struct.unpack('<H', rec[0:2])[0]
        serviceType_byte = rec[14]
        if serviceType_byte in (25, 0x11, 0x19): sType = "HD"
        elif serviceType_byte == 2: sType = "Radio"
        else: sType = "SD"
        name_bytes = rec[36:36+96]
        name = name_bytes.decode('utf-16be', errors='ignore').split('\0')[0]
        
        # Tersine Mühendislik (ChanSort tabanlı):
        is_encrypted = (rec[136] & 0x01) != 0
        encrypted = "Yes" if is_encrypted else "No"
        
        is_locked = (rec[13] & 0x01) != 0
        fav1 = struct.unpack('<i', rec[140:144])[0] > 0
        fav2 = struct.unpack('<i', rec[144:148])[0] > 0
        fav3 = struct.unpack('<i', rec[148:152])[0] > 0
        fav4 = struct.unpack('<i', rec[152:156])[0] > 0
        fav5 = struct.unpack('<i', rec[156:160])[0] > 0
        
        tp_index = struct.unpack('<H', rec[18:20])[0]
        freq_info = tp_dict.get(tp_index, {'freq': '???', 'sym': '???', 'pol': '?'})
        
        channels.append({
            'Slot': i // 168, 
            'No': channelNo, 
            'Name': name, 
            'Type': sType, 
            'Encrypted': encrypted, 
            'Freq': freq_info['freq'], 
            'Pol': freq_info['pol'], 
            'Sym': freq_info['sym'],
            'Lock': is_locked,
            'Fav1': fav1,
            'Fav2': fav2,
            'Fav3': fav3,
            'Fav4': fav4,
            'Fav5': fav5
        })
    channels.sort(key=lambda x: x['No'])
    return channels

def build_scm_direct(original_scm, new_scm, edited_channels):
    try:
        with zipfile.ZipFile(original_scm, 'r') as zin:
            with zipfile.ZipFile(new_scm, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    data = zin.read(item.filename)
                    if item.filename == 'map-SateD':
                        out_data = bytearray()
                        active_records = []
                        for i in range(0, len(data), 168):
                            rec = bytearray(data[i:i+168])
                            if len(rec) < 168: break
                            slot = i // 168
                            if slot in edited_channels:
                                edits = edited_channels[slot]
                                struct.pack_into('<H', rec, 0, edits['No'])
                                name_bytes = edits['Name'].encode('utf-16be')[:94]
                                for j in range(96): rec[36+j] = 0
                                rec[36:36+len(name_bytes)] = name_bytes
                                
                                # Lock Flag (Offset 13)
                                if edits.get('Lock', False):
                                    rec[13] |= 0x01
                                else:
                                    rec[13] &= ~0x01
                                
                                # Encrypted Flag (Offset 136)
                                if edits.get('Encrypted') == 'Yes':
                                    rec[136] |= 0x01
                                else:
                                    rec[136] &= ~0x01
                                
                                # Fav 1-5 Flags
                                fav1_val = edits['No'] if edits.get('Fav1', False) else -1
                                fav2_val = edits['No'] if edits.get('Fav2', False) else -1
                                fav3_val = edits['No'] if edits.get('Fav3', False) else -1
                                fav4_val = edits['No'] if edits.get('Fav4', False) else -1
                                fav5_val = edits['No'] if edits.get('Fav5', False) else -1
                                
                                struct.pack_into('<i', rec, 140, fav1_val)
                                struct.pack_into('<i', rec, 144, fav2_val)
                                struct.pack_into('<i', rec, 148, fav3_val)
                                struct.pack_into('<i', rec, 152, fav4_val)
                                struct.pack_into('<i', rec, 156, fav5_val)
                                
                                active_records.append(rec)
                        for rec in active_records:
                            csum = sum(rec[:167]) % 256
                            rec[167] = csum
                            out_data.extend(rec)
                        padding_len = len(data) - len(out_data)
                        if padding_len > 0:
                            out_data.extend(b'\x00' * padding_len)
                        zout.writestr(item, out_data)
                    else:
                        zout.writestr(item, data)
        return True
    except Exception as e:
        print(f"Build error: {e}")
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Kullanım:")
        print("  Çıkart : python3 scm_cli.py extract <orijinal.scm> <kanallar.csv>")
        print("  Oluştur: python3 scm_cli.py build <orijinal.scm> <kanallar.csv> <yeni_liste.scm>")
        sys.exit(1)
        
    mode = sys.argv[1]
    
    if mode == "extract" and len(sys.argv) == 4:
        extract_to_csv(sys.argv[2], sys.argv[3])
    elif mode == "build" and len(sys.argv) == 5:
        build_from_csv(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("Hatalı parametre girdiniz.")

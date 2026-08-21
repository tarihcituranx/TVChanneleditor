**Ultimo aggiornamento:** 21/08/2026

# 📺 TV Channel Editor

> **Editor di elenchi di canali TV multimarca** — Un'unica piattaforma per Samsung, LG, Sony, Hisense e molti altri.

[![Demo dal vivo](https://img.shields.io/badge/🌐_Canlı_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![Licenza: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENZA)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue)](https://python.org)

---

## 🎯 Cosa fa?

È possibile modificare visivamente nel browser il file con l’elenco dei canali trasferito dalla TV sulla porta USB tramite **drag-and-drop** e ricaricarlo sulla TV. **I dati vengono conservati solo temporaneamente (RAM/Temp) durante l’operazione e non vengono salvati in modo permanente.**

---

## 📺 Marche di TV supportate

| Marca | Formato | Stato |
|-------|--------|-------|
| **Samsung** (Serie E/F/H) | `.scm` | ✅ Supporto completo |
| **Samsung** (J/K/M/Q/R/T - Tizen) | `.zip` (SQLite) | ✅ Supporto completo |
| **LG** (webOS 5+) | `.tll` (XML) | ✅ Supporto completo |
| **Sony BRAVIA** | `sdb.xml` | ✅ Supporto completo |
| **Hisense** (2017+) | `servicelist.db` | ✅ Supporto completo |
| **Panasonic VIERA** | `svl.db / svl.bin` | 🔄 Versione beta |
| Philips, Toshiba, Grundig... | `*.db / *.xml` | 🔜 Prossimamente |

## 🛰️ Satelliti supportati

**Türksat 4A/5B** · **Hotbird 13E** · **Astra 19.2E** · e tutti gli altri satelliti DVB-S

---

## ✨ Funzionalità

- **🪄 Bacchetta magica** — Applica i modelli Generale / Notizie / Sport con un solo clic
- **🛠️ Generatore di modelli** — Crea e salva la tua lista ideale
- **📱 Trasferimento al dispositivo tramite codice** — Trasferisci facilmente l’elenco dei canali dal cellulare vicino alla TV al computer tramite un codice di 8 caratteri
- **🔍 Verifica automatica delle frequenze** — Rileva automaticamente le frequenze obsolete o errate (Türksat)
- **⭐ Preferiti e Blocco** — Gestione dei preferiti da 1 a 5 e blocco bambini
- **🗑️ Operazioni in blocco** — Elimina in blocco i canali criptati, le stazioni radio o gli elementi selezionati
- **🌙 Tema scuro/chiaro e 👁️ Modalità per daltonici** — Interfaccia accessibile a tutti
- **🌐 11 lingue disponibili** — Supporto per turco e inglese
- **📊 Privacy totale (analisi senza cookie)** — Statistiche integrate che non utilizzano cookie né dati personali
- **📱 Completamente reattivo** — Compatibile con desktop, tablet e dispositivi mobili

---

## 🚀 Utilizzo in tempo reale

Utilizzabile direttamente nel browser senza alcuna installazione:

👉 **[tvchanneleditor.onrender.com](https://tvchanneleditor.onrender.com)**

---

## 💻 Installazione locale

```bash
git clone https://github.com/tarihcituranx/TVChanneleditor.git
cd TVChanneleditor
pip install -r requirements.txt
python3 app.py
```

Vai all'indirizzo `http://127.0.0.1:5000` nel browser.

---

## 🏗️ Struttura del progetto

```
├── app.py # Applicazione principale Flask e header di sicurezza
├── scm_core.py # Motore Samsung SCM (binario)
├── tizen_core.py # Motore Samsung Tizen SQLite
├── lg_core.py # Motore LG GlobalClone XML
├── sony_core.py # Motore sdb.xml di Sony
├── hisense_core.py     # Motore SQLite di Hisense
├── templates/ # Modelli HTML Jinja2 (11 lingue)
├── static/
│   ├── css/style.css   # Tema scuro/chiaro + tutti gli stili
│   ├── js/app.js # Frontend (drag-and-drop, rendering dei canali, template)
│   └── data/ # frequenze.json, templates.json
```

---

## 🔐 Sicurezza

- Tutti gli header di sicurezza sono attivi (CSP, HSTS, CORP, COOP, Referrer-Policy...)
- Limite di dimensione dei file: 2 MB
- I file caricati vengono eliminati dopo l’elaborazione
- Nessun dato dei canali viene registrato sul server
- Contatto per la sicurezza: `tarihcituranx@proton.me`

---

## 🤖 Guida all’intelligenza artificiale

Se state sviluppando con l’assistente AI, leggete il file [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md).

---

## 🔌 Utilizzo dell’API per sviluppatori e degli agenti IA (Developer API)

Questo progetto non è solo un sito web, ma è stato progettato anche come una **API REST** completa che gli agenti di intelligenza artificiale (AI Agents) e gli sviluppatori possono utilizzare direttamente tramite codice.

> 🧑‍💻 **Per gli sviluppatori:** potete consultare la documentazione interattiva di Swagger UI all’indirizzo [tvchanneleditor.onrender.com/api/docs](https://tvchanneleditor.onrender.com/api/docs).
> 
> 🤖 **Per gli agenti AI (ChatGPT, Claude, ecc.):** Potete fornire all’intelligenza artificiale lo schema OpenAPI in testo semplice (plain-text) leggibile dalla macchina tramite questo link: [tvchanneleditor.onrender.com/api/openapi.txt](https://tvchanneleditor.onrender.com/api/openapi.txt)



### Verifica della versione e del deploy (Version Check)
Per verificare in un attimo se il server di rendering ha pubblicato l'ultimo commit su GitHub o se è ancora in cache:
```bash
curl -sS https://tvchanneleditor.onrender.com/api/version
```
```json
{
  "status": "online",
  "version": "1.0.0",
  "commit": "abc1234...",
  "deployed_at": "2026-08-21T19:00:51.123Z"
}
```

---

## 🙏 Grazie

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — Prima fonte di ispirazione
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — Riferimento di reverse engineering per SCM e formati multibrand
- **[Türksat Satellite](https://uydu.turksat.com.tr/)** — Database di verifica delle frequenze Türksat

---

## 📄 Licenza

Distribuito come software open source sotto licenza MIT.

> "Samsung", "LG", "Sony", "Hisense", "Panasonic" e i relativi loghi sono marchi registrati delle rispettive società. Questo è uno strumento comunitario indipendente e open source.

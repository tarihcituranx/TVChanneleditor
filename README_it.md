[🇹🇷 TR](README.md) | [🇺🇸 EN](README_en.md) | [🇩🇪 DE](README_de.md) | [🇷🇺 RU](README_ru.md) | [🇪🇸 ES](README_es.md) | [🇮🇹 IT](README_it.md) | [🇫🇷 FR](README_fr.md) | [🇸🇦 AR](README_ar.md) | [🇮🇷 FA](README_fa.md) | [🇦🇿 AZ](README_az.md) | [🇵🇹 PT](README_pt.md)

**Ultimo aggiornamento:** 21/08/2026

# 📺 Editor dei canali TV

> **Editor di elenchi di canali TV multimarca** — Modifica i tuoi elenchi di canali TV Samsung, LG, Sony e Hisense direttamente dal browser.

[![Demo dal vivo](https://img.shields.io/badge/🌐_Canlı_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![Documentazione API](https://img.shields.io/badge/API-Swagger_UI-orange)](https://tvchanneleditor.onrender.com/api/docs)
[![CI](https://github.com/tarihcituranx/TVChanneleditor/actions/workflows/test.yml/badge.svg)](https://github.com/tarihcituranx/TVChanneleditor/actions)
[![Licenza: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENZA)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org)

---

## ✨ A cosa serve?

È uno strumento open source che consente di modificare visivamente, tramite **drag-and-drop** nel browser, il file dell'elenco dei canali che la TV trasferisce su una chiavetta USB. Non richiede installazione, funziona direttamente dal browser o tramite l'API REST.

## 👤 Chi può utilizzarlo?

- Chi desidera modificare l’elenco dei canali della TV Samsung dal computer
- Chi desidera modificare i file XML `.tll` di LG GlobalClone
- Chi lavora con gli elenchi `sdb.xml` di Sony e `servicelist.db` di Hisense
- Gli sviluppatori che desiderano modificare la lista dei canali in modo programmatico
- Chi desidera automatizzare la lista dei canali tramite un agente AI

## 📺 Formati supportati (Matrice di compatibilità)

| Formato | Lettura | Modifica | Ricreazione | Nota |
|--------|:---:|:---:|:---:|-----|
| **Samsung `.scm`** | ✅ | ✅ | ✅ | Serie E/F/H (binario) |
| **Samsung Tizen `.zip`** | ✅ | ✅ | ✅ | Serie J/K/M/Q/R/T (SQLite) |
| **Sony `sdb.xml`** | ✅ | ✅ | ✅ | Serie BRAVIA |
| **Hisense `servicelist.db`** | ✅ | ✅ | ✅ | Modelli 2017 e 2021 |
| **LG XML `.tll`** | ✅ | ✅ | ✅ | Solo GlobalClone XML (il formato binario non è supportato) |
| **Panasonic `svl.*`** | 🔜 | 🔜 | 🔜 | In programma / In fase di sviluppo |

> **⚠️ Nota importante sulla compatibilità con LG:** I file **binari .tll** di vecchia generazione di LG non sono supportati. È possibile elaborare solo i file `.tll` di nuova generazione basati su XML (GlobalClone). Per i file precedenti è necessario utilizzare l’applicazione desktop *ChanSort*.


## ⚠️ Limitazioni importanti

Prima dell'utilizzo, si prega di tenere presenti le seguenti limitazioni tecniche:
- **LG Binary TLL:** I file binari `.tll` di vecchia generazione non sono supportati.
- **Panasonic SVL:** Il supporto è in fase di sviluppo (in programma).
- **Verifica della frequenza:** È attiva solo per i dati satellitari Türksat.
- **Limite di dimensione dei file:** i file caricati possono avere una dimensione massima di **2 MB**.
- **Sessione temporanea:** i file non vengono salvati in modo permanente, ma vengono automaticamente cancellati al termine della sessione.

## 🚀 Guida rapida

1. **Trasferisci dalla TV alla chiavetta USB:** dal menu della TV (Trasmissione > Impostazioni avanzate) trasferisci l’elenco dei canali su una chiavetta USB formattata in FAT32.
2. **Carica:** trascina e rilascia il file dalla chiavetta USB sul sito.
3. **Modifica:** ordina i canali con il drag-and-drop, elimina quelli non necessari o utilizza 💡 i modelli intelligenti.
4. **Scarica:** scarica nuovamente il file modificato sul tuo computer.
5. **Carica sulla TV:** ricollega la chiavetta USB alla TV e importa la nuova lista.

## 🛰️ Supporto per satelliti e frequenze

Le liste dei canali **DVB-S/S2** possono essere elaborate senza problemi dal punto di vista del formato. **La funzione di verifica automatica delle frequenze (rilevamento di frequenze obsolete/errate) è attualmente attiva solo per i dati di Türksat 4A/5B.** Gli altri satelliti (Hotbird, Astra ecc.) sono pienamente supportati per l’ordinamento e la modifica.

---

## 🔌 Come funziona l’API per sviluppatori (REST)?

È disponibile un semplice flusso in 3 passaggi per gli agenti AI e gli sviluppatori. Per ulteriori dettagli, è possibile consultare i link [Swagger UI](https://tvchanneleditor.onrender.com/api/docs) o [Schema OpenAPI](https://tvchanneleditor.onrender.com/api/openapi.txt).

**Passo 1: Caricamento (Upload)**
```http
POST /upload
Content-Type: multipart/form-data
```
*(Come risposta viene restituito un `session_id` e un elenco JSON dei canali)*

**Passaggio 2: Creazione (Build)**
```http
POST /build
Content-Type: application/json
{
  "session_id": "uuid-...",
  "channels": [ ... elenco modificato ... ]
}
```
*(Come risposta viene restituito il link `/download/...` da cui è possibile scaricare il file)*

**Passaggio 3: Download**
```http
GET /download/{session_id}/{filename}
```
*(Viene scaricato il file binario/archivio modificato)*

## 🔐 Privacy e sicurezza

- È previsto un limite di **2 MB** per le dimensioni dei file.
- **I file non vengono archiviati in modo permanente sul server.** I file caricati vengono elaborati nella memoria temporanea del server per tutta la durata della sessione di modifica, non vengono archiviati in modo permanente e vengono automaticamente cancellati per intero allo scadere della sessione (circa 1 ora).
- Non è prevista alcuna registrazione di account, iscrizione o database.
- Le operazioni di parsing XML sull’API (a protezione dagli attacchi Billion Laughs) sono protette tramite `defusedxml`.

## 🧪 Sistema di test (CI)

Il progetto presenta un’architettura di test **Round-Trip (Andata e ritorno)**.
- Utilizzando file di test realistici (fixtures), si verifica che il codice del motore, anche se danneggiato o modificato, non comprometta le strutture originali del database TV.
- Ad ogni operazione `push` e `PR`, su GitHub Actions viene eseguito automaticamente il file `tests/test_roundtrip.py`.

## 🌍 Supporto linguistico

L’interfaccia e le guide all’uso sono disponibili in **11 lingue**: turco, inglese, tedesco, russo, spagnolo, italiano, francese, arabo, persiano, azero e portoghese.

## 🏗️ Struttura del progetto

```
├── app.py # Server Flask, percorsi API e i18n
├── scm_core.py # Motore SCM Samsung
├── tizen_core.py # Motore SQLite Samsung Tizen
├── lg_core.py # Motore XML LG
├── sony_core.py # Motore XML Sony
├── hisense_core.py     # Motore SQLite Hisense
├── templates/ # Interfacce HTML Jinja2 (11 lingue)
├── static/ # CSS, JS, schemi YAML OpenAPI
└── tests/
    ├── test_roundtrip.py  # Test di andata e ritorno per tutti i motori
    └── fixtures/ # Esempi di database TV reali per i test
```

## 🙏 Grazie

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — Fonte di ispirazione iniziale
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — Riferimento di reverse engineering per i formati di più marche
- **[Türksat Satellite](https://uydu.turksat.com.tr/)** — Database delle frequenze Türksat

## 📄 Licenza

Distribuito come software open source sotto licenza MIT.
> «Samsung», «LG», «Sony», «Hisense», «Panasonic» e i relativi loghi sono marchi registrati delle rispettive società. Questo è uno strumento indipendente e open source sviluppato dalla comunità.

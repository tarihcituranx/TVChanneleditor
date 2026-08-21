[🇹🇷 TR](README.md) | [🇺🇸 EN](README_en.md) | [🇩🇪 DE](README_de.md) | [🇷🇺 RU](README_ru.md) | [🇪🇸 ES](README_es.md) | [🇮🇹 IT](README_it.md) | [🇫🇷 FR](README_fr.md) | [🇸🇦 AR](README_ar.md) | [🇮🇷 FA](README_fa.md) | [🇦🇿 AZ](README_az.md) | [🇵🇹 PT](README_pt.md)

**Letzte Aktualisierung:** 21.08.2026

# 📺 TV-Kanal-Editor

> **Editor für TV-Kanallisten verschiedener Marken** — Bearbeiten Sie Ihre TV-Kanallisten für Samsung, LG, Sony und Hisense über Ihren Browser.

[![Live-Demo](https://img.shields.io/badge/🌐_Canlı_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![API-Dokumentation](https://img.shields.io/badge/API-Swagger_UI-orange)](https://tvchanneleditor.onrender.com/api/docs)
[![CI](https://github.com/tarihcituranx/TVChanneleditor/actions/workflows/test.yml/badge.svg)](https://github.com/tarihcituranx/TVChanneleditor/actions)
[![Lizenz: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org)

---

## ✨ Wozu dient es?

Ein Open-Source-Tool, mit dem Sie die von Ihrem Fernseher auf einen USB-Stick kopierte Kanallisten-Datei per **Drag-and-Drop** in Ihrem Browser visuell bearbeiten können. Es erfordert keine Installation und läuft direkt im Browser oder über die REST-API.

## 👤 Wer kann es nutzen?

- Alle, die die Samsung-TV-Kanalliste vom Computer aus bearbeiten möchten
- Alle, die LG GlobalClone-XML-`.tll`-Dateien bearbeiten möchten
- Alle, die mit Sony-`.sdb.xml`- und Hisense-`.servicelist.db`-Listen arbeiten
- Entwickler, die die Senderliste programmgesteuert ändern möchten
- Nutzer, die die Senderliste mithilfe von KI-Agenten (AI Agent) automatisieren möchten

## 📺 Unterstützte Formate (Kompatibilitätsmatrix)

| Format | Lesen | Bearbeiten | Neu erstellen | Anmerkung |
|--------|:---:|:---:|:---:|-----|
| **Samsung `.scm`** | ✅ | ✅ | ✅ | E/F/H-Serie (Binär) |
| **Samsung Tizen `.zip`** | ✅ | ✅ | ✅ | J/K/M/Q/R/T-Serie (SQLite) |
| **Sony `sdb.xml`** | ✅ | ✅ | ✅ | BRAVIA-Serie |
| **Hisense `servicelist.db`** | ✅ | ✅ | ✅ | Modelle von 2017 und 2021 |
| **LG XML `.tll`** | ✅ | ✅ | ✅ | Nur GlobalClone XML (Binärdateien werden nicht unterstützt) |
| **Panasonic `svl.*`** | 🔜 | 🔜 | 🔜 | Geplant / In Entwicklung |

> **⚠️ Wichtiger Hinweis zur LG-Kompatibilität:** LGs **binäre .tll**-Dateien der alten Generation werden nicht unterstützt. Es können nur XML-basierte (GlobalClone) `.tll`-Dateien der neuen Generation verarbeitet werden. Für ältere Dateien müssen Sie die Desktop-Anwendung *ChanSort* verwenden.


## ⚠️ Wichtige Einschränkungen

Bitte beachten Sie vor der Nutzung die folgenden technischen Einschränkungen:
- **LG Binary TLL:** Binäre `.tll`-Dateien der alten Generation werden nicht unterstützt.
- **Panasonic SVL:** Die Unterstützung befindet sich in der Entwicklungsphase (geplant).
- **Frequenzüberprüfung:** Ist nur für Türksat-Satellitendaten aktiv.
- **Dateigrößenbeschränkung:** Hochgeladene Dateien dürfen maximal **2 MB** groß sein.
- **Temporäre Sitzung:** Dateien werden nicht dauerhaft gespeichert, sondern nach Ende der Sitzung automatisch gelöscht.

## 🚀 Schnellstart

1. **Vom Fernseher auf USB übertragen:** Übertragen Sie die Senderliste über das TV-Menü (Sendung > Experteneinstellungen) auf einen im FAT32-Format formatierten USB-Stick.
2. **Hochladen:** Ziehen Sie die Datei vom USB-Stick per Drag & Drop auf die Website.
3. **Bearbeiten:** Sortieren Sie die Einträge per Drag & Drop, löschen Sie nicht benötigte Einträge oder nutzen Sie 💡 die intelligenten Vorlagen.
4. **Herunterladen:** Laden Sie die bearbeitete Datei wieder auf Ihren Computer herunter.
5. **Auf den Fernseher laden:** Stecken Sie den USB-Stick wieder in den Fernseher und importieren Sie die neue Liste.

## 🛰️ Satelliten- und Frequenzunterstützung

**DVB-S/S2**-Kanallisten, die von den unterstützten Engines (Marken) bereitgestellt werden, können verarbeitet werden. **Die Funktion zur automatischen Frequenzüberprüfung (Erkennung veralteter/falscher Frequenzen) ist derzeit nur für Türksat 4A/5B-Daten aktiv.** Andere Satelliten (Hotbird, Astra usw.) werden für die Sortierung und Bearbeitung vollständig unterstützt.

---

## 🔌 Wie funktioniert die Entwickler-API (REST)?

Für KI-Agenten und Entwickler gibt es einen einfachen 3-Schritte-Ablauf. Weitere Details finden Sie unter [Swagger UI](https://tvchanneleditor.onrender.com/api/docs) oder [OpenAPI-Schema](https://tvchanneleditor.onrender.com/api/openapi.txt).

**Schritt 1: Hochladen (Upload)**
```http
POST /upload
Content-Type: multipart/form-data
```
*(Als Antwort werden eine `session_id` und eine JSON-Liste der Kanäle zurückgegeben)*

**Schritt 2: Erstellen (Build)**
```http
POST /build
Content-Type: application/json
{
  "session_id": "uuid-...",
  "channels": [ ... sortierte Liste ... ]
}
```
*(Als Antwort wird der Link `/download/...` zurückgegeben, über den die Datei heruntergeladen werden kann)*

**Schritt 3: Herunterladen (Download)**
```http
GET /download/{session_id}/{filename}
```
*(Die bearbeitete Binär- bzw. Archivdatei wird heruntergeladen)*

## 🔐 Datenschutz und Sicherheit

- Es gilt eine Dateigrößenbeschränkung von **2 MB**.
- **Dateien werden nicht dauerhaft auf dem Server gespeichert.** Hochgeladene Dateien werden während der Bearbeitungssitzung im temporären Serverspeicher verarbeitet, nicht dauerhaft archiviert und nach Ablauf der Sitzungsdauer (ca. 1 Stunde) automatisch vollständig gelöscht.
- Es erfolgt keine Protokollierung von Konten, Mitgliedschaften oder Datenbanken.
- XML-Parsing-Vorgänge über die API (zum Schutz vor „Billion Laughs“-Angriffen) werden durch `defusedxml` geschützt.

## 🧪 Testsystem (CI)

Das Projekt verfügt über eine **Round-Trip-Testarchitektur**.
- Mithilfe von realistischen Testdateien (Fixtures) wird geprüft, dass fehlerhafter oder geänderter Engine-Code die ursprünglichen Strukturen der TV-Datenbank nicht beeinträchtigt.
- Bei jedem `Push` und jeder `PR` wird `tests/test_roundtrip.py` automatisch über GitHub Actions ausgeführt.

## 🌍 Sprachunterstützung

Die Benutzeroberfläche und die Bedienungsanleitungen sind in **11 Sprachen** verfügbar: Türkisch, Englisch, Deutsch, Russisch, Spanisch, Italienisch, Französisch, Arabisch, Persisch, Aserbaidschanisch und Portugiesisch.

## 🏗️ Projektstruktur

```
├── app.py # Flask-Server, API-Routen und i18n
├── scm_core.py # Samsung-SCM-Engine
├── tizen_core.py # Samsung-Tizen-SQLite-Engine
├── lg_core.py # LG-XML-Engine
├── sony_core.py # Sony-XML-Engine
├── hisense_core.py     # Hisense-SQLite-Engine
├── templates/ # Jinja2-HTML-Oberflächen (11 Sprachen)
├── static/ # CSS, JS, OpenAPI-YAML-Schemas
└── tests/
    ├── test_roundtrip.py  # Roundtrip-Tests für alle Engines
    └── fixtures/ # Echte TV-Datenbankbeispiele für Tests
```

## 🙏 Vielen Dank

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — Erste Inspirationsquelle
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — Reverse-Engineering-Referenz für Formate verschiedener Marken
- **[Türksat-Satellit](https://uydu.turksat.com.tr/)** — Türksat-Frequenzdatenbank

## 📄 Lizenz

Wird als Open Source unter der MIT-Lizenz bereitgestellt.
> „Samsung“, „LG“, „Sony“, „Hisense“, „Panasonic“ und die entsprechenden Logos sind eingetragene Marken der jeweiligen Unternehmen. Dies ist ein unabhängiges Open-Source-Community-Tool.

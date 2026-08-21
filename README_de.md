[🇹🇷 TR](README.md) | [🇺🇸 EN](README_en.md) | [🇩🇪 DE](README_de.md) | [🇷🇺 RU](README_ru.md) | [🇪🇸 ES](README_es.md) | [🇮🇹 IT](README_it.md) | [🇫🇷 FR](README_fr.md) | [🇸🇦 AR](README_ar.md) | [🇮🇷 FA](README_fa.md) | [🇦🇿 AZ](README_az.md) | [🇵🇹 PT](README_pt.md)

**Letzte Aktualisierung:** 21.08.2026

# 📺 TV-Kanal-Editor

> **Editor für TV-Kanallisten verschiedener Marken** — Eine einzige Plattform für Samsung, LG, Sony, Hisense und mehr.

[![Live-Demo](https://img.shields.io/badge/🌐_Live_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![CI](https://github.com/tarihcituranx/TVChanneleditor/actions/workflows/test.yml/badge.svg)](https://github.com/tarihcituranx/TVChanneleditor/actions)
[![Lizenz: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org)
[![API-Dokumentation](https://img.shields.io/badge/API-Swagger_UI-orange)](https://tvchanneleditor.onrender.com/api/docs)

---

## 🎯 Was macht das Programm?

Sie können die von Ihrem Fernseher auf den USB-Stick kopierte Kanallisten-Datei im Browser per **Drag & Drop** visuell bearbeiten und anschließend wieder auf den Fernseher hochladen. **Die Daten werden nur während des Vorgangs vorübergehend (im RAM/Temp) gespeichert und nicht dauerhaft aufbewahrt.**

---

## 📺 Unterstützte TV-Marken

| Marke | Format | Status |
|-------|--------|-------|
| **Samsung** (E/F/H-Serie) | `.scm` | ✅ Vollständige Unterstützung |
| **Samsung** (J/K/M/Q/R/T – Tizen) | `.zip` (SQLite) | ✅ Vollständige Unterstützung |
| **LG** (webOS 5+) | `.tll` (XML) | ✅ Vollständige Unterstützung |
| **Sony BRAVIA** | `sdb.xml` | ✅ Vollständige Unterstützung |
| **Hisense** (ab 2017) | `servicelist.db` | ✅ Vollständige Unterstützung |
| **Panasonic VIERA** | `svl.db / svl.bin` | 🔄 Beta |
| Philips, Toshiba, Grundig... | `*.db / *.xml` | 🔜 Demnächst |

## 🛰️ Unterstützte Satelliten

**Türksat 4A/5B** · **Hotbird 13E** · **Astra 19,2E** · und alle anderen DVB-S-Satelliten

---

## ✨ Funktionen

- **💡 Intelligente Vorlagen** — Wenden Sie Vorlagen für „Allgemein“, „Nachrichten“ und „Sport“ mit einem Klick an
- **🛠️ Vorlagen-Generator** — Erstellen und speichern Sie Ihre eigene ideale Liste
- **📱 Übertragung auf das Gerät per Code** — Übertragen Sie die Senderliste ganz einfach mit einem 8-stelligen Code vom Handy neben dem Fernseher auf den Computer
- **🔍 Automatische Frequenzüberprüfung** — Erkennt automatisch veraltete/falsche Frequenzen (Türksat)
- **⭐ Favoriten & Kindersicherung** — Favoriten 1–5 und Kindersicherung einrichten
- **🗑️ Massenaktionen** — Verschlüsselte Kanäle, Radiosender oder ausgewählte Einträge in einem Schritt löschen
- **🌙 Dunkles/helles Design & 👁️ Modus für Farbenblindheit** — Barrierefreie Benutzeroberfläche für alle
- **🌐 Unterstützung für 11 Sprachen**
- **📊 Vollständige Privatsphäre (Cookie-freie Analyse)** — Integrierte Statistiken ohne Verwendung von Cookies oder personenbezogenen Daten
- **📱 Vollständig responsiv** — Kompatibel mit Desktop, Tablet und Mobilgeräten

---

## 🚀 Live-Nutzung

Nutzen Sie es direkt im Browser, ganz ohne Installation:

👉 **[tvchanneleditor.onrender.com](https://tvchanneleditor.onrender.com)**

---

## 💻 Lokale Installation

```bash
git clone https://github.com/tarihcituranx/TVChanneleditor.git
cd TVChanneleditor
pip install -r requirements.txt
python3 app.py
```

Rufen Sie im Browser die Adresse `http://127.0.0.1:5000` auf.

---

## 🏗️ Projektstruktur

```
├── app.py # Flask-Hauptanwendung & Sicherheits-Header
├── scm_core.py # Samsung SCM (Binär)-Engine
├── tizen_core.py # Samsung Tizen SQLite-Engine
├── lg_core.py # LG GlobalClone XML-Engine
├── sony_core.py # Sony sdb.xml-Engine
├── hisense_core.py     # Hisense SQLite-Engine
├── templates/ # Jinja2-HTML-Vorlagen (11 Sprachen)
├── static/
│   ├── css/style.css   # Dark/Light-Design + alle Stile
│   ├── js/app.js # Frontend (Drag-and-Drop, Kanal-Rendering, Vorlage)
│   └── data/ # frekanslar.json, templates.json
```

---

## 🔐 Sicherheit

- Alle Sicherheits-Header sind aktiviert (CSP, HSTS, CORP, COOP, Referrer-Policy...)
- Dateigrößenbeschränkung: 2 MB
- Hochgeladene Dateien werden nach der Verarbeitung gelöscht
- Es werden keinerlei Kanaldaten auf dem Server protokolliert
- Sicherheitskontakt: `tarihcituranx@proton.me`

---

## 🤖 Leitfaden zur künstlichen Intelligenz

Wenn Sie mit dem KI-Assistenten entwickeln, lesen Sie bitte die Datei [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md).

---

## 🔌 Nutzung der Entwickler-API und des KI-Agenten (Developer API)

Dieses Projekt ist nicht nur eine Website, sondern wurde auch als vollwertige **REST-API** konzipiert, die KI-Agenten (AI Agents) und Entwickler direkt über Code nutzen können.

> 🧑‍💻 **Für Entwickler:** Die interaktive Swagger-UI-Dokumentation finden Sie unter [tvchanneleditor.onrender.com/api/docs](https://tvchanneleditor.onrender.com/api/docs).
> 
> 🤖 **Für KI-Agenten (ChatGPT, Claude usw.):** Sie können dem KI-System das maschinenlesbare OpenAPI-Schema im Klartext (Plain-Text) über den folgenden Link zur Verfügung stellen: [tvchanneleditor.onrender.com/api/openapi.txt](https://tvchanneleditor.onrender.com/api/openapi.txt)



### Versions- und Deployment-Überprüfung (Version Check)
Um in Sekundenschnelle zu testen, ob der Render-Server den aktuellen GitHub-Commit in Produktion übernommen hat oder ob er noch im Cache verbleibt:
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

## 🙏 Vielen Dank

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — Erste Inspirationsquelle
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — Referenz für Reverse Engineering von SCM- und Multi-Brand-Formaten
- **[Türksat-Satellit](https://uydu.turksat.com.tr/)** — Datenbank zur Überprüfung der Türksat-Frequenzen

---

## 📄 Lizenz

Wird als Open Source unter der MIT-Lizenz bereitgestellt.

> „Samsung“, „LG“, „Sony“, „Hisense“, „Panasonic“ und die entsprechenden Logos sind eingetragene Marken der jeweiligen Unternehmen. Dies ist ein unabhängiges Open-Source-Community-Tool.

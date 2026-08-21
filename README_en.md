**Last Updated:** August 21, 2026

# 📺 TV Channel Editor

> **Multi-brand TV channel list editor** — A single platform for Samsung, LG, Sony, Hisense, and more.

[![Live Demo](https://img.shields.io/badge/🌐_Canlı_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue)](https://python.org)

---

## 🎯 What Does It Do?

You can visually edit the channel list file transferred by your TV to a USB drive using **drag-and-drop** in your browser and then reload it onto your TV. **Data is only temporarily stored (in RAM/Temp) during the process; it is not saved permanently.**

---

## 📺 Supported TV Brands

| Brand | Format | Status |
|-------|--------|-------|
| **Samsung** (E/F/H Series) | `.scm` | ✅ Full Support |
| **Samsung** (J/K/M/Q/R/T - Tizen) | `.zip` (SQLite) | ✅ Full Support |
| **LG** (webOS 5+) | `.tll` (XML) | ✅ Full Support |
| **Sony BRAVIA** | `sdb.xml` | ✅ Full Support |
| **Hisense** (2017+) | `servicelist.db` | ✅ Full Support |
| **Panasonic VIERA** | `svl.db / svl.bin` | 🔄 Beta |
| Philips, Toshiba, Grundig... | `*.db / *.xml` | 🔜 Coming Soon |

## 🛰️ Supported Satellites

**Türksat 4A/5B** · **Hotbird 13E** · **Astra 19.2E** · and all other DVB-S satellites

---

## ✨ Features

- **🪄 Magic Wand** — Apply General / News / Sports templates with a single click
- **🛠️ Template Creator** — Create and save your own ideal list
- **📱 Transfer to Device via Code** — Easily transfer the channel list from your smartphone next to the TV to your computer using an 8-character code
- **🔍 Automatic Frequency Verification** — Automatically detects old or incorrect frequencies (Türksat)
- **⭐ Favorites & Lock** — Manage Favorites 1–5 and the child lock
- **🗑️ Bulk Actions** — Delete encrypted channels, radio stations, or selected items in bulk
- **🌙 Dark/Light Theme & 👁️ Color Blind Mode** — An accessible interface for everyone
- **🌐 11 Language Options** — Supports Turkish and English
- **📊 Full Privacy (Cookie-Free Analytics)** — Built-in statistics that do not use cookies or personal data
- **📱 Fully Responsive** — Compatible with desktop, tablet, and mobile

---

## 🚀 Live Demo

Use it directly in your browser without any setup:

👉 **[tvchanneleditor.onrender.com](https://tvchanneleditor.onrender.com)**

---

## 💻 Local Installation

```bash
git clone https://github.com/tarihcituranx/TVChanneleditor.git
cd TVChanneleditor
pip install -r requirements.txt
python3 app.py
```

Go to `http://127.0.0.1:5000` in your browser.

---

## 🏗️ Project Structure

```
├── app.py # Flask main application & security headers
├── scm_core.py # Samsung SCM (binary) engine
├── tizen_core.py # Samsung Tizen SQLite engine
├── lg_core.py # LG GlobalClone XML engine
├── sony_core.py # Sony sdb.xml engine
├── hisense_core.py     # Hisense SQLite engine
├── templates/ # Jinja2 HTML templates (11 languages)
├── static/
│   ├── css/style.css   # Dark/Light theme + all styles
│   ├── js/app.js # Frontend (drag-and-drop, channel rendering, templates)
│   └── data/ # frequencies.json, templates.json
```

---

## 🔐 Security

- All security headers are enabled (CSP, HSTS, CORP, COOP, Referrer-Policy...)
- File size limit: 2MB
- Uploaded files are deleted after processing
- No channel data is logged on the server
- Security contact: `tarihcituranx@proton.me`

---

## 🤖 AI Guide

If you’re developing with the AI assistant, read the [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md) file.

---

## 🔌 Using the Developer API & AI Agents

This project is not just a website; it’s also designed as a full-featured **REST API** that AI agents and developers can use directly via code.

> 🧑‍💻 **For Developers:** You can view the interactive Swagger UI documentation at [tvchanneleditor.onrender.com/api/docs](https://tvchanneleditor.onrender.com/api/docs).
> 
> 🤖 **For AI Agents (ChatGPT, Claude, etc.):** You can provide the system’s machine-readable Plain-Text OpenAPI schema to the AI via this link: [tvchanneleditor.onrender.com/api/openapi.txt](https://tvchanneleditor.onrender.com/api/openapi.txt)


For this to work, you must add the authorized API keys to your server’s (or computer’s) environment variables:
```bash
export VALID_API_KEYS="secret-key-1,secret-key-2"
```

### 4. Version and Deployment Verification (Version Check)
To instantly test whether the render server has deployed the latest GitHub commit or is still running from the cache:
```bash
curl -sS https://tvchanneleditor.onrender.com/api/version
```
```json
{
  "status": "online",
  "version": "1.0.0",
  "commit": "97401a5...",
  "deployed_at": "2026-08-18T19:00:51.123Z"
}
```

---

## 🙏 Thanks

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — Initial source of inspiration
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — Reverse engineering reference for SCM + multi-brand formats
- **[Türksat Satellite](https://uydu.turksat.com.tr/)** — Türksat frequency verification database

---

## 📄 License

Released as open source under the MIT License.

> “Samsung,” “LG,” “Sony,” “Hisense,” “Panasonic,” and their logos are registered trademarks of their respective companies. This is an independent, open-source community tool.

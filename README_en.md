[🇹🇷 TR](README.md) | [🇺🇸 EN](README_en.md) | [🇩🇪 DE](README_de.md) | [🇷🇺 RU](README_ru.md) | [🇪🇸 ES](README_es.md) | [🇮🇹 IT](README_it.md) | [🇫🇷 FR](README_fr.md) | [🇸🇦 AR](README_ar.md) | [🇮🇷 FA](README_fa.md) | [🇦🇿 AZ](README_az.md) | [🇵🇹 PT](README_pt.md)

**Last Updated:** 2026-08-21

# 📺 TV Channel Editor

> **Multi-brand TV channel list editor** — Edit your Samsung, LG, Sony, and Hisense TV channel lists directly in your browser.

[![Live Demo](https://img.shields.io/badge/🌐_Demo-tvchanneleditor.onrender.com_en_-blue)](https://tvchanneleditor.onrender.com/en/)
[![API Docs](https://img.shields.io/badge/API-Swagger_UI-orange)](https://tvchanneleditor.onrender.com/api/docs)
[![CI](https://github.com/tarihcituranx/TVChanneleditor/actions/workflows/test.yml/badge.svg)](https://github.com/tarihcituranx/TVChanneleditor/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org)

---

## ✨ What Does It Do?

It is an open-source tool that allows you to visually edit the channel list file transferred by your TV to a USB drive using the **drag-and-drop** method in your browser. It requires no installation and runs directly in the browser or via the REST API.

## 👤 Who Can Use It?

- Those who want to edit the Samsung TV channel list from a computer
- Those who want to edit LG GlobalClone XML `.tll` files
- Those working with Sony `sdb.xml` and Hisense `servicelist.db` lists
- Developers who want to modify the channel list programmatically
- Those who want to automate channel list management using AI agents

## 📺 Supported Formats (Compatibility Matrix)

| Format | Read | Edit | Regenerate | Note |
|--------|:---:|:---:|:---:|-----|
| **Samsung `.scm`** | ✅ | ✅ | ✅ | E/F/H Series (Binary) |
| **Samsung Tizen `.zip`** | ✅ | ✅ | ✅ | J/K/M/Q/R/T Series (SQLite) |
| **Sony `sdb.xml`** | ✅ | ✅ | ✅ | BRAVIA Series |
| **Hisense `servicelist.db`** | ✅ | ✅ | ✅ | 2017 and 2021 Models |
| **LG XML `.tll`** | ✅ | ✅ | ✅ | GlobalClone XML only (Binary not supported) |
| **Panasonic `svl.*`** | 🔜 | 🔜 | 🔜 | Planned / In development |

> **⚠️ Important LG Compatibility Note:** LG’s older-generation **binary .tll** files are not supported. Only the newer XML-based (GlobalClone) `.tll` files can be processed. For older files, you must use the desktop *ChanSort* application.


## ⚠️ Important Limitations

Please keep the following technical limitations in mind before using the app:
- **LG Binary TLL:** Older-generation binary `.tll` files are not supported.
- **Panasonic SVL:** Support is under development (Planned).
- **Frequency Verification:** Active only for Türksat satellite data.
- **File Size Limit:** Uploaded files can be a maximum of **2 MB**.
- **Temporary Session:** Files are not stored permanently; they are automatically deleted at the end of the session.

## 🚀 Quick Start

1. **Transfer from TV to USB:** From the TV menu (Broadcast > Expert Settings), transfer the channel list to a FAT32-formatted USB drive.
2. **Upload:** Drag and drop the file from the USB drive onto the website.
3. **Edit:** Reorder using drag-and-drop, delete unnecessary items, or use 💡 Smart Templates.
4. **Download:** Download the edited file back to your computer.
5. **Install on TV:** Reinsert the USB drive into the TV and import the new list.

## 🛰️ Satellite and Frequency Support

**DVB-S/S2** channel lists provided by supported engines (brands) can be processed. **The automatic frequency verification feature (detecting outdated or incorrect frequencies) is currently active only for Türksat 4A/5B data.** Other satellites (Hotbird, Astra, etc.) are fully supported for sorting and editing.

---

## 🔌 How Does the Developer API (REST) Work?

There is a simple 3-step workflow for AI agents and developers. For more details, see the [Swagger UI](https://tvchanneleditor.onrender.com/api/docs) or [OpenAPI Schema](https://tvchanneleditor.onrender.com/api/openapi.txt) links.

**Step 1: Upload**
```http
POST /upload
Content-Type: multipart/form-data
```
*(Returns a `session_id` and a JSON list of channels in the response)*

**Step 2: Build**
```http
POST /build
Content-Type: application/json
{
  "session_id": "uuid-...",
  "channels": [ ... formatted list ... ]
}
```
*(Returns a `/download/...` link where the file can be downloaded)*

**Step 3: Download**
```http
GET /download/{session_id}/{filename}
```
*(The processed binary/archive file is downloaded)*

## 🔐 Privacy and Security

- There is a **2 MB** file size limit.
- **Files are not permanently stored on the server.** Uploaded files are processed in temporary server storage for the duration of the editing session; they are not permanently archived and are automatically and completely deleted when the session expires (approximately 1 hour).
- There is no account, membership, or database logging.
- XML parsing operations on the API (to protect against Billion Laughs attacks) are secured using `defusedxml`.

## 🧪 Test System (CI)

The project features a **Round-Trip** testing architecture.
- Using real-world test files (fixtures), we verify that broken or modified engine code does not corrupt the original TV database structures.
- With every `push` and `PR`, `tests/test_roundtrip.py` runs automatically on GitHub Actions.

## 🌍 Language Support

The interface and user guides are available in **11 languages**: Turkish, English, German, Russian, Spanish, Italian, French, Arabic, Persian, Azerbaijani, and Portuguese.

## 🏗️ Project Structure

```
├── app.py # Flask server, API routes, and i18n
├── scm_core.py # Samsung SCM engine
├── tizen_core.py # Samsung Tizen SQLite engine
├── lg_core.py # LG XML engine
├── sony_core.py # Sony XML engine
├── hisense_core.py     # Hisense SQLite engine
├── templates/ # Jinja2 HTML interfaces (11 languages)
├── static/ # CSS, JS, OpenAPI YAML schemas
└── tests/
    ├── test_roundtrip.py  # Round-trip tests for all engines
    └── fixtures/ # Real TV database samples for tests
```

## 🙏 Thanks

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — Initial source of inspiration
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — Reverse-engineering reference for multi-brand formats
- **[Türksat Satellite](https://uydu.turksat.com.tr/)** — Türksat frequency database

## 📄 License

Released as open source under the MIT License.
> “Samsung,” “LG,” “Sony,” “Hisense,” “Panasonic,” and their logos are registered trademarks of their respective companies. This is an independent, open-source community tool.

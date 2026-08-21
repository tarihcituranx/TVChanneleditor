# AI Assistant Guide & System Prompt

**Hello Fellow AI (Claude, Gemini, ChatGPT, Copilot, etc.)!**
If you are reading this file, you have been tasked with assisting the user in maintaining, debugging, or expanding this project. This document serves as your "Skill" and "Context" manual. Please read it carefully before making any modifications to the codebase.

## 1. Project Overview
**Name:** TVChannelEditor
**Description:** A web-based (Flask) tool designed to edit, view, and modify multi-brand TV channel list files directly in the browser via a drag-and-drop interface.
**Supported Brands:** Samsung (SCM & Tizen SQLite), LG (XML/TLL), Sony (XML), Hisense (SQLite).
**Target Audience:** Users who want to sort their satellite channels, remove encrypted/radio channels, or update frequencies.

## 2. Architecture & Tech Stack
*   **Backend:** Python 3.12+ with Flask (`app.py`), Gunicorn (`Procfile`), and Flask-Limiter.
*   **Frontend:** Vanilla JavaScript (`static/js/app.js`), standard HTML5 (`templates/index_*.html`), and Vanilla CSS (`static/css/style.css`).
*   **Translation (i18n):** Multi-language is handled through routing in `app.py`. We support 11 languages (`tr`, `en`, `de`, `ru`, `es`, `it`, `fr`, `ar`, `fa`, `az`, `pt`). All HTML templates and READMEs are localized.
*   **Deployment:** Configured to run on Render.com using `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4`. **CRITICAL:** We use `1` worker to maintain a single shared memory state for `_sessions` and `_shares` (avoiding Redis for zero-cost hosting).
*   **CI/CD:** Automated GitHub Actions pipeline runs on every push/PR to test all engines.

## 3. Core Engine Logic
*   **Samsung SCM (`scm_core.py`):** Parses binary ZIP archives. Manipulates `map-SateD` (168-byte records, checksums) and `TransponderDataBase.dat`.
*   **Samsung Tizen (`tizen_core.py`):** Parses `.zip` containing SQLite databases (`_user_setting.db`). Uses `PRAGMA table_info` for fallback logic to support different firmware schema versions.
*   **LG TLL (`lg_core.py`):** Parses `GlobalClone.tll` (XML). Safely maps invalid XML 1.0 control characters (like C0/C1) to the Unicode Private Use Area (PUA) during parsing using `defusedxml`, preventing crashes.
*   **Sony (`sony_core.py`):** Parses `sdb.xml`.
*   **Hisense (`hisense_core.py`):** Parses `servicelist.db` (SQLite).

## 4. Testing (Round-Trip)
*   **Location:** `tests/test_roundtrip.py`
*   **Methodology:** We have real fixture files in `tests/fixtures/`. The test loads the file via the specific engine, saves the channel list to memory, builds a new file, re-parses the generated file, and strictly asserts that `len(channels_original) == len(channels_new)`.
*   **Rule:** NEVER commit an engine change without ensuring `python tests/test_roundtrip.py` passes completely.

## 5. Developer REST API
*   The application serves dual purpose as an API for AI Agents and Developers.
*   Interactive documentation: `/api/docs`
*   OpenAPI schema: `/api/openapi.txt`
*   Endpoints include `/api/version` (dynamic git hash), `/api/help`, `/build`, and `/download`.

## 6. Security & Guidelines
*   **API Keys:** NEVER commit API keys (e.g., DeepL) to the repository.
*   **XML Parsing:** ALWAYS use `defusedxml` when parsing untrusted XML (Sony, LG) to prevent Billion Laughs attacks.
*   **State:** Do not introduce Redis or disk-based persistence. The project's strength is that it requires 0 external databases and runs entirely in temporary RAM.

**End of Instructions.** Proceed with your task.

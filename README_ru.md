[🇹🇷 TR](README.md) | [🇺🇸 EN](README_en.md) | [🇩🇪 DE](README_de.md) | [🇷🇺 RU](README_ru.md) | [🇪🇸 ES](README_es.md) | [🇮🇹 IT](README_it.md) | [🇫🇷 FR](README_fr.md) | [🇸🇦 AR](README_ar.md) | [🇮🇷 FA](README_fa.md) | [🇦🇿 AZ](README_az.md) | [🇵🇹 PT](README_pt.md)

**Последнее обновление:** 21.08.2026

# 📺 TV Channel Editor

> **Редактор списка телеканалов для различных брендов** — единая платформа для Samsung, LG, Sony, Hisense и других.

[![Онлайн-демо](https://img.shields.io/badge/🌐_Canlı_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![CI](https://github.com/tarihcituranx/TVChanneleditor/actions/workflows/test.yml/badge.svg)](https://github.com/tarihcituranx/TVChanneleditor/actions)
[![Лицензия: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org)

---

## 🎯 Что делает?

Вы можете визуально редактировать файл со списком каналов, перенесённый с телевизора на USB, в браузере с помощью **перетаскивания**, а затем снова загрузить его на телевизор. **Данные хранятся только временно (в оперативной памяти/временных файлах) во время обработки и не сохраняются на постоянной основе.**

---

## 📺 Поддерживаемые марки телевизоров

| Марка | Формат | Статус |
|-------|--------|-------|
| **Samsung** (серии E/F/H) | `.scm` | ✅ Полная поддержка |
| **Samsung** (J/K/M/Q/R/T — Tizen) | `.zip` (SQLite) | ✅ Полная поддержка |
| **LG** (webOS 5+) | `.tll` (XML) | ✅ Полная поддержка |
| **Sony BRAVIA** | `sdb.xml` | ✅ Полная поддержка |
| **Hisense** (2017+) | `servicelist.db` | ✅ Полная поддержка |
| **Panasonic VIERA** | `svl.db / svl.bin` | 🔄 Бета-версия |
| Philips, Toshiba, Grundig... | `*.db / *.xml` | 🔜 Скоро |

## 🛰️ Поддерживаемые спутники

**Türksat 4A/5B** · **Hotbird 13E** · **Astra 19.2E** · и все остальные спутники DVB-S

---

## ✨ Особенности

- **🪄 Волшебная палочка** — примените шаблоны «Общие», «Новости» и «Спорт» одним щелчком
- **🛠️ Конструктор шаблонов** — создайте и сохраните свой идеальный список
- **📱 Перенос на устройство с помощью кода** — легко переносите список каналов с мобильного телефона, находящегося рядом с телевизором, на компьютер с помощью 8-символьного кода
- **🔍 Автоматическая проверка частот** — автоматически обнаруживает устаревшие/неверные частоты (Türksat)
- **⭐ Избранное и блокировка** — настройка избранного (1–5) и детской блокировки
- **🗑️ Массовые действия** — массовое удаление зашифрованных каналов, радиостанций или выбранных элементов
- **🌙 Тёмная/светлая тема и 👁️ Режим для людей с цветовой слепотой** — интерфейс, доступный для всех
- **🌐 11 языков** — поддержка турецкого и английского языков
- **📊 Полная конфиденциальность (аналитика без файлов cookie)** — встроенная статистика, не использующая файлы cookie или личные данные
- **📱 Полная адаптивность** — совместимость с настольными компьютерами, планшетами и мобильными устройствами

---

## 🚀 Использование в режиме реального времени

Используйте прямо в браузере без какой-либо установки:

👉 **[tvchanneleditor.onrender.com](https://tvchanneleditor.onrender.com)**

---

## 💻 Локальная установка

```bash
git clone https://github.com/tarihcituranx/TVChanneleditor.git
cd TVChanneleditor
pip install -r requirements.txt
python3 app.py
```

Перейдите в браузере по адресу `http://127.0.0.1:5000`.

---

## 🏗️ Структура проекта

```
├── app.py # Главное приложение Flask и заголовки безопасности
├── scm_core.py # Драйвер Samsung SCM (бинарный)
├── tizen_core.py # Драйвер Samsung Tizen SQLite
├── lg_core.py # Драйвер LG GlobalClone XML
├── sony_core.py # Драйвер Sony sdb.xml
├── hisense_core.py     # Драйвер Hisense SQLite
├── templates/ # HTML-шаблоны Jinja2 (11 языков)
├── static/
│   ├── css/style.css   # Тёмная/светлая тема + все стили
│   ├── js/app.js # Фронтенд (перетаскивание, рендеринг каналов, шаблоны)
│   └── data/ # frekanslar.json, templates.json
```

---

## 🔐 Безопасность

- Все заголовки безопасности активны (CSP, HSTS, CORP, COOP, Referrer-Policy...)
- Ограничение по размеру файла: 2 МБ
- Загруженные файлы удаляются после обработки
- Данные каналов не регистрируются в журналах сервера
- Контакт по вопросам безопасности: `tarihcituranx@proton.me`

---

## 🤖 Руководство по искусственному интеллекту

Если вы занимаетесь разработкой с помощью ИИ-помощника, ознакомьтесь с файлом [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md).

---

## 🔌 Использование API для разработчиков и ИИ-агентов (Developer API)

Этот проект представляет собой не только веб-сайт, но и полнофункциональный **REST API**, который ИИ-агенты (AI Agents) и разработчики могут использовать напрямую в коде.

> 🧑‍💻 **Для разработчиков:** Вы можете ознакомиться с интерактивной документацией Swagger UI по адресу [tvchanneleditor.onrender.com/api/docs](https://tvchanneleditor.onrender.com/api/docs).
> 
> 🤖 **Для AI-агентов (ChatGPT, Claude и т. д.):** Вы можете предоставить системе машиночитаемую схему OpenAPI в виде простого текста (Plain-Text) для искусственного интеллекта по следующей ссылке: [tvchanneleditor.onrender.com/api/openapi.txt](https://tvchanneleditor.onrender.com/api/openapi.txt)



### Проверка версии и развертывания (Version Check)
Чтобы за считанные секунды проверить, был ли опубликован последний коммит сервера рендеринга на GitHub или он остался в кэше:
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

## 🙏 Спасибо

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — Первый источник вдохновения
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — справочник по реверс-инжинирингу для SCM и форматов нескольких брендов
- **[Türksat Uydu](https://uydu.turksat.com.tr/)** — база данных для проверки частот Türksat

---

## 📄 Лицензия

Проект предоставляется в качестве открытого исходного кода по лицензии MIT.

> «Samsung», «LG», «Sony», «Hisense», «Panasonic» и их логотипы являются зарегистрированными товарными знаками соответствующих компаний. Это независимый инструмент с открытым исходным кодом, разработанный сообществом.

[🇹🇷 TR](README.md) | [🇺🇸 EN](README_en.md) | [🇩🇪 DE](README_de.md) | [🇷🇺 RU](README_ru.md) | [🇪🇸 ES](README_es.md) | [🇮🇹 IT](README_it.md) | [🇫🇷 FR](README_fr.md) | [🇸🇦 AR](README_ar.md) | [🇮🇷 FA](README_fa.md) | [🇦🇿 AZ](README_az.md) | [🇵🇹 PT](README_pt.md)

**آخرین به‌روزرسانی:** ۲۱ اوت ۲۰۲۶

# 📺 ویرایشگر کانال تلویزیون

> **ویرایشگر لیست کانال تلویزیون چند-برند** — یک پلتفرم واحد برای سامسونگ، ال‌جی، سونی، هایسنس و غیره.

[![دموی زنده](https://img.shields.io/badge/🌐_Live_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![CI](https://github.com/tarihcituranx/TVChanneleditor/actions/workflows/test.yml/badge.svg)](https://github.com/tarihcituranx/TVChanneleditor/actions)
[![مجوز: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENCE)
[![پایتون ۳.۱۲+](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org)
[![مستندات API](https://img.shields.io/badge/API-Swagger_UI-orange)](https://tvchanneleditor.onrender.com/api/docs)

---

## 🎯 این چه کاری انجام می‌دهد؟

شما می‌توانید فایل لیست کانال‌ها را که توسط تلویزیون شما به یک درایو USB منتقل شده است، با استفاده از **کشیدن و رها کردن** در مرورگر خود به صورت بصری ویرایش کرده و سپس آن را دوباره روی تلویزیون بارگذاری کنید. **داده‌ها فقط به طور موقت (در رم/موقت) در طول فرآیند ذخیره می‌شوند؛ و به طور دائم ذخیره نمی‌شوند.**

---

## 📺 برندهای تلویزیون پشتیبانی‌شده

| برند | فرمت | وضعیت |
|-------|--------|-------|
| **سامسونگ** (سری E/F/H) | `.scm` | ✅ پشتیبانی کامل |
| **سامسونگ** (J/K/M/Q/R/T – تایزن) | `.zip` (SQLite) | ✅ پشتیبانی کامل |
| **LG** (webOS 5+) | `.tll` (XML) | ✅ پشتیبانی کامل |
| **Sony BRAVIA** | `sdb.xml` | ✅ پشتیبانی کامل |
| **Hisense** (۲۰۱۷+) | `servicelist.db` | ✅ پشتیبانی کامل |
| **Panasonic VIERA** | `svl.db / svl.bin` | 🔄 بتا |
| فیلیپس، توشیبا، گروندیگ... | `*.db / *.xml` | 🔜 به‌زودی |

## 🛰️ ماهواره‌های پشتیبانی‌شده

**تورک‌ست ۴A/۵B** · **هات‌برد ۱۳E** · **آسترا ۱۹.۲E** · و سایر ماهواره‌های DVB-S

---

## ✨ ویژگی‌ها

- **💡 قالب‌های هوشمند** — با یک کلیک قالب‌های عمومی / اخبار / ورزش را اعمال کنید
- **🛠️ سازنده قالب** — لیست کانال ایده‌آل خود را ایجاد و ذخیره کنید
- **📱 انتقال به دستگاه از طریق کد** — به راحتی لیست کانال‌ها را از تلفن همراه خود که در کنار تلویزیون قرار دارد، با استفاده از یک کد ۸ کاراکتری به رایانه خود منتقل کنید
- **🔍 تأیید خودکار فرکانس** — به طور خودکار فرکانس‌های منسوخ یا نادرست را تشخیص می‌دهد (تورک‌ست)
- **⭐ موارد دلخواه و قفل** — مدیریت موارد دلخواه ۱ تا ۵ و قفل کودک
- **🗑️ عملیات دسته‌ای** — حذف دسته‌ای کانال‌های رمزگذاری‌شده، ایستگاه‌های رادیویی یا موارد منتخب
- **🌙 تم تاریک/روشن و حالت 👁️ رنگ‌آبی** — رابط کاربری در دسترس برای همه
- **🌐 پشتیبانی از ۱۱ زبان**
- **📊 حریم خصوصی کامل (تحلیل بدون کوکی)** — آمار داخلی که از کوکی‌ها یا داده‌های شخصی استفاده نمی‌کند
- **📱 کاملاً واکنش‌گرا** — سازگار با دسکتاپ، تبلت و موبایل

---

## 🚀 نسخه نمایشی زنده

آن را مستقیماً در مرورگر خود بدون نیاز به نصب استفاده کنید:

👉 **[tvchanneleditor.onrender.com](https://tvchanneleditor.onrender.com)**

---

## 💻 نصب محلی

```bash
git clone https://github.com/tarihcituranx/TVChanneleditor.git
cd TVChanneleditor
pip install -r requirements.txt
python3 app.py
```

به `http://127.0.0.1:5000` در مرورگر خود بروید.

---

## 🏗️ ساختار پروژه

```
├── app.py # برنامه اصلی Flask و هدرهای امنیتی
├── scm_core.py # موتور SCM سامسونگ (بای‌نری)
├── tizen_core.py # موتور SQLite تایزن سامسونگ
├── lg_core.py # موتور XML GlobalClone ال‌جی
├── sony_core.py # موتور sdb.xml سونی
├── hisense_core.py     # موتور SQLite هایسنس
├── templates/ # قالب‌های HTML جینجا۲ (۱۱ زبان)
├── static/
│   ├── css/style.css   # تم تیره/روشن + تمام استایل‌ها
│   ├── js/app.js # فرانت‌اند (کشیدن و رها کردن، رندر کانال، قالب‌ها)
│   └── data/ # frequencies.json, templates.json
```

---

## 🔐 امنیت

- تمام هدرهای امنیتی فعال هستند (CSP, HSTS, CORP, COOP, Referrer-Policy...)
- محدودیت اندازه فایل: ۲ مگابایت
- فایل‌های آپلود شده پس از پردازش حذف می‌شوند
- هیچ داده‌ای از کانال‌ها روی سرور ثبت نمی‌شود
- تماس امنیتی: `tarihcituranx@proton.me`

---

## 🤖 راهنمای هوش مصنوعی

اگر با دستیار هوش مصنوعی در حال توسعه هستید، لطفاً فایل [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md) را بخوانید.

---

## 🔌 استفاده از API توسعه‌دهنده و ربات‌های هوش مصنوعی

این پروژه فقط یک وب‌سایت نیست؛ بلکه به عنوان یک **API REST** کاملاً جامع نیز طراحی شده است که ربات‌های هوش مصنوعی و توسعه‌دهندگان می‌توانند مستقیماً از طریق کد از آن استفاده کنند.

> 🧑‍💻 **برای توسعه‌دهندگان:** می‌توانید مستندات تعاملی Swagger UI را در [tvchanneleditor.onrender.com/api/docs](https://tvchanneleditor.onrender.com/api/docs) مشاهده کنید.
> 
> 🤖 **برای ربات‌های هوش مصنوعی (چت‌جی‌پی‌تی، کلود و غیره):** شما می‌توانید طرحواره OpenAPI متن-ساده قابل خواندن توسط ماشین این سیستم را از طریق این لینک در اختیار هوش مصنوعی قرار دهید: [tvchanneleditor.onrender.com/api/openapi.txt](https://tvchanneleditor.onrender.com/api/openapi.txt)



### تأیید نسخه و استقرار (بررسی نسخه)
برای آزمایش فوری اینکه آیا آخرین commit گیت‌هاب (GitHub) سرور رندر مستقر شده است یا هنوز در حافظه پنهان (cached) قرار دارد:
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

## 🙏 تشکر

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — منبع الهام اولیه
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — مرجع مهندسی معکوس برای SCM و فرمت‌های چند برند
- **[ماهواره Türksat](https://uydu.turksat.com.tr/)** — پایگاه داده تأیید فرکانس Türksat

---

## 📄 مجوز

به‌عنوان نرم‌افزار متن‌باز تحت مجوز MIT منتشر شده است.

> «سامسونگ»، «ال‌جی»، «سونی»، «هایسنس»، «پاناسونیک» و لوگوهای آن‌ها علائم تجاری ثبت‌شده شرکت‌های مربوطه هستند. این یک ابزار مستقل و متن‌باز جامعه است.

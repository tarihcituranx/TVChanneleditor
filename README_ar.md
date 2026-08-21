[🇹🇷 TR](README.md) | [🇺🇸 EN](README_en.md) | [🇩🇪 DE](README_de.md) | [🇷🇺 RU](README_ru.md) | [🇪🇸 ES](README_es.md) | [🇮🇹 IT](README_it.md) | [🇫🇷 FR](README_fr.md) | [🇸🇦 AR](README_ar.md) | [🇮🇷 FA](README_fa.md) | [🇦🇿 AZ](README_az.md) | [🇵🇹 PT](README_pt.md)

**آخر تحديث:** 21 أغسطس 2026

# 📺 محرر قنوات التلفزيون

> **محرر قائمة قنوات التلفزيون متعددة العلامات التجارية** — منصة واحدة لأجهزة سامسونج وإل جي وسوني وهيسنس وغيرها.

[![عرض توضيحي مباشر](https://img.shields.io/badge/🌐_Canlı_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![CI](https://github.com/tarihcituranx/TVChanneleditor/actions/workflows/test.yml/badge.svg)](https://github.com/tarihcituranx/TVChanneleditor/actions)
[![الترخيص: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org)

---

## 🎯 ما الذي يفعله؟

يمكنك تحرير ملف قائمة القنوات الذي ينقله التلفزيون إلى USB بصريًا في المتصفح باستخدام **السحب والإفلات**، ثم إعادة تحميله إلى التلفزيون. **يتم الاحتفاظ بالبيانات مؤقتًا (RAM/Temp) أثناء العملية فقط، ولا يتم تخزينها بشكل دائم.**

---

## 📺 العلامات التجارية للتلفزيونات المدعومة

| العلامة التجارية | التنسيق | الحالة |
|-------|--------|-------|
| **Samsung** (سلسلة E/F/H) | `.scm` | ✅ دعم كامل |
| **Samsung** (J/K/M/Q/R/T - Tizen) | `.zip` (SQLite) | ✅ دعم كامل |
| **LG** (webOS 5+) | `.tll` (XML) | ✅ دعم كامل |
| **Sony BRAVIA** | `sdb.xml` | ✅ دعم كامل |
| **Hisense** (2017+) | `servicelist.db` | ✅ دعم كامل |
| **Panasonic VIERA** | `svl.db / svl.bin` | 🔄 بيتا |
| Philips، Toshiba، Grundig... | `*.db / *.xml` | 🔜 قريبًا |

## 🛰️ الأقمار الصناعية المدعومة

**Türksat 4A/5B** · **Hotbird 13E** · **Astra 19.2E** · وجميع الأقمار الصناعية DVB-S الأخرى

---

## ✨ الميزات

- **🪄 العصا السحرية** — قم بتطبيق قوالب «عام» / «أخبار» / «رياضة» بنقرة واحدة
- **🛠️ منشئ القوالب** — أنشئ قائمتك المثالية واحفظها
- **📱 النقل إلى الجهاز باستخدام رمز** — انقل قائمة القنوات بسهولة من الهاتف المحمول الموجود بجانب التلفزيون إلى الكمبيوتر باستخدام رمز مكون من 8 أحرف
- **🔍 التحقق التلقائي من التردد** — يكتشف الترددات القديمة/الخاطئة تلقائيًا (Türksat)
- **⭐ المفضلة و«قفل الأطفال»** — تنظيم القنوات المفضلة من 1 إلى 5 وقفل الأطفال
- **🗑️ العمليات الجماعية** — احذف القنوات المشفرة أو محطات الراديو أو العناصر المحددة دفعة واحدة
- **🌙 سمة داكنة/فاتحة & 👁️ وضع عمى الألوان** — واجهة سهلة الاستخدام للجميع
- **🌐 11 خيارًا للغة** — دعم اللغتين التركية والإنجليزية
- **📊 خصوصية تامة (تحليلات بدون ملفات تعريف الارتباط)** — إحصائيات مدمجة لا تستخدم ملفات تعريف الارتباط أو البيانات الشخصية
- **📱 متوافق تمامًا مع جميع الأجهزة** — متوافق مع أجهزة الكمبيوتر المكتبية والأجهزة اللوحية والهواتف المحمولة

---

## 🚀 الاستخدام المباشر

استخدمه مباشرةً في المتصفح دون الحاجة إلى أي تثبيت:

👉 **[tvchanneleditor.onrender.com](https://tvchanneleditor.onrender.com)**

---

## 💻 التثبيت المحلي

```bash
git clone https://github.com/tarihcituranx/TVChanneleditor.git
cd TVChanneleditor
pip install -r requirements.txt
python3 app.py
```

انتقل إلى العنوان `http://127.0.0.1:5000` في المتصفح.

---

## 🏗️ بنية المشروع

```
├── app.py # التطبيق الرئيسي لـ Flask ورؤوس الأمان
├── scm_core.py # محرك Samsung SCM (ثنائي)
├── tizen_core.py # محرك Samsung Tizen SQLite
├── lg_core.py # محرك LG GlobalClone XML
├── sony_core.py # محرك sdb.xml الخاص بـ Sony
├── hisense_core.py     # محرك SQLite الخاص بـ Hisense
├── templates/ # قوالب HTML لـ Jinja2 (11 لغة)
├── static/
│   ├── css/style.css   # سمة داكنة/فاتحة + جميع الأنماط
│   ├── js/app.js # الواجهة الأمامية (السحب والإفلات، عرض القنوات، القوالب)
│   └── data/ # frekanslar.json، templates.json
```

---

## 🔐 الأمان

- جميع رؤوس الأمان نشطة (CSP، HSTS، CORP، COOP، Referrer-Policy...)
- الحد الأقصى لحجم الملف: 2 ميغابايت
- يتم حذف الملفات التي تم تحميلها بعد معالجتها
- لا يتم تسجيل أي بيانات قنوات في سجلات الخادم
- جهة الاتصال الخاصة بالأمن: `tarihcituranx@proton.me`

---

## 🤖 دليل الذكاء الاصطناعي

إذا كنت تقوم بالتطوير باستخدام مساعد الذكاء الاصطناعي، فاقرأ ملف [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md).

---

## 🔌 استخدام واجهة برمجة التطبيقات للمطورين (Developer API) ووكيل الذكاء الاصطناعي (AI Agent)

هذا المشروع ليس مجرد موقع ويب، بل صُمم أيضًا ليكون **واجهة برمجة تطبيقات REST** كاملة يمكن لوكلاء الذكاء الاصطناعي (AI Agents) والمطورين استخدامها مباشرةً عبر الكود.

> 🧑‍💻 **للمطورين:** يمكنكم الاطلاع على وثائق Swagger UI التفاعلية على الرابط [tvchanneleditor.onrender.com/api/docs](https://tvchanneleditor.onrender.com/api/docs).
> 
> 🤖 **بالنسبة لوكلاء الذكاء الاصطناعي (ChatGPT، Claude، إلخ):** يمكنكم تزويد الذكاء الاصطناعي بمخطط OpenAPI بنص عادي (Plain-Text) قابل للقراءة آليًا عبر الرابط التالي: [tvchanneleditor.onrender.com/api/openapi.txt](https://tvchanneleditor.onrender.com/api/openapi.txt)



### التحقق من الإصدار والنشر (Version Check)
للتحقق في غضون ثوانٍ مما إذا كان خادم العرض قد نشر أحدث إصدار من Github Commit أم لا، أو ما إذا كان لا يزال موجودًا في ذاكرة التخزين المؤقتة:
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

## 🙏 شكرًا

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — مصدر الإلهام الأول
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — مرجع الهندسة العكسية لتنسيقات SCM + العلامات التجارية المتعددة
- **[Türksat Uydu](https://uydu.turksat.com.tr/)** — قاعدة بيانات التحقق من ترددات Türksat

---

## 📄 الترخيص

تم تقديمه كمصدر مفتوح بموجب ترخيص MIT.

> «Samsung» و«LG» و«Sony» و«Hisense» و«Panasonic» وشعاراتها هي علامات تجارية مسجلة للشركات المعنية. هذا أداة مجتمعية مستقلة ومفتوحة المصدر.

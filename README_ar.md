[🇹🇷 TR](README.md) | [🇺🇸 EN](README_en.md) | [🇩🇪 DE](README_de.md) | [🇷🇺 RU](README_ru.md) | [🇪🇸 ES](README_es.md) | [🇮🇹 IT](README_it.md) | [🇫🇷 FR](README_fr.md) | [🇸🇦 AR](README_ar.md) | [🇮🇷 FA](README_fa.md) | [🇦🇿 AZ](README_az.md) | [🇵🇹 PT](README_pt.md)

**آخر تحديث:** 2026-08-21

# 📺 محرر قنوات التلفزيون

> **محرر قوائم قنوات التلفزيون متعددة العلامات التجارية** — قم بتنظيم قوائم قنوات التلفزيون الخاصة بك من Samsung و LG و Sony و Hisense عبر المتصفح.

[![عرض توضيحي مباشر](https://img.shields.io/badge/🌐_Canlı_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![وثائق واجهة برمجة التطبيقات](https://img.shields.io/badge/API-Swagger_UI-orange)](https://tvchanneleditor.onrender.com/api/docs)
[![CI](https://github.com/tarihcituranx/TVChanneleditor/actions/workflows/test.yml/badge.svg)](https://github.com/tarihcituranx/TVChanneleditor/actions)
[![الترخيص: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org)

---

## ✨ ما فائدته؟

إنه أداة مفتوحة المصدر تتيح لك تعديل ملف قائمة القنوات الذي ينقله تلفازك إلى ذاكرة USB بصريًا في متصفحك باستخدام طريقة **السحب والإفلات**. لا يتطلب التثبيت، ويعمل مباشرةً عبر المتصفح أو واجهة برمجة التطبيقات REST.

## 📺 التنسيقات المدعومة (مصفوفة التوافق)

| التنسيق | القراءة | التحرير | إعادة الإنشاء | ملاحظة |
|--------|:---:|:---:|:---:|-----|
| **Samsung `.scm`** | ✅ | ✅ | ✅ | سلسلة E/F/H (ثنائي) |
| **Samsung Tizen `.zip`** | ✅ | ✅ | ✅ | سلسلة J/K/M/Q/R/T (SQLite) |
| **سوني `sdb.xml`** | ✅ | ✅ | ✅ | سلسلة BRAVIA |
| **هيسنس `servicelist.db`** | ✅ | ✅ | ✅ | طرازات 2017 و2021 |
| **LG XML `.tll`** | ✅ | ✅ | ✅ | GlobalClone XML فقط (لا يدعم التنسيق الثنائي) |
| **Panasonic `svl.*`** | 🔜 | 🔜 | 🔜 | مخطط / قيد التطوير |

> **⚠️ ملاحظة مهمة بشأن توافق LG:** لا يتم دعم ملفات **Binary .tll** من الجيل القديم الخاصة بـ LG. يمكن معالجة ملفات `.tll` المستندة إلى XML (GlobalClone) من الجيل الجديد فقط. بالنسبة للملفات القديمة، يجب عليك استخدام تطبيق *ChanSort* المخصص لأجهزة الكمبيوتر المكتبية.

## 🚀 البدء السريع

1. **انقل من التلفزيون إلى USB:** انقل قائمة القنوات من قائمة التلفزيون (البث > الإعدادات المتقدمة) إلى USB بتنسيق FAT32.
2. **قم بالتحميل:** اسحب الملف الموجود على USB وأفلته على الموقع.
3. **التنظيم:** قم بالترتيب بالسحب والإفلات، أو احذف العناصر غير الضرورية، أو استخدم 💡 القوالب الذكية.
4. **التنزيل:** قم بتنزيل الملف المنظم مرة أخرى على جهاز الكمبيوتر الخاص بك.
5. **التحميل على التلفزيون:** أعد توصيل وحدة USB بالتلفزيون واستورد القائمة الجديدة.

## 🛰️ دعم الأقمار الصناعية والترددات

يمكن معالجة قوائم قنوات **DVB-S/S2** دون أي مشاكل من حيث التنسيق. **ميزة التحقق التلقائي من الترددات (الكشف عن الترددات القديمة/الخاطئة) نشطة حاليًا لبيانات Türksat 4A/5B فقط.** أما الأقمار الصناعية الأخرى (Hotbird، Astra، إلخ)، فهي مدعومة بالكامل للترتيب والتنظيم.

---

## 🔌 كيف تعمل واجهة برمجة التطبيقات (API) للمطورين (REST)؟

يتوفر مسار بسيط من 3 خطوات لوكلاء الذكاء الاصطناعي والمطورين. لمزيد من التفاصيل، يمكنك الرجوع إلى روابط [Swagger UI](https://tvchanneleditor.onrender.com/api/docs) أو [مخطط OpenAPI](https://tvchanneleditor.onrender.com/api/openapi.txt).

**الخطوة 1: التحميل (Upload)**
```http
POST /upload
Content-Type: multipart/form-data
```
*(يُرجع `session_id` وقائمة القنوات بتنسيق JSON كرد)*

**الخطوة 2: الإنشاء (Build)**
```http
POST /build
Content-Type: application/json
{
  "session_id": "uuid-...",
  "channels": [ ... قائمة منظمة ... ]
}
```
*(يُرجع كاستجابة رابط `/download/...` الذي يمكن من خلاله تنزيل الملف)*

**الخطوة 3: التنزيل (Download)**
```http
GET /download/{session_id}/{filename}
```
*(يتم تنزيل الملف الثنائي/المضغوط الذي تم تعديله)*

## 🔐 الخصوصية والأمان

- يوجد حد لحجم الملف يبلغ **2 ميغابايت**.
- **لا يتم تخزين الملفات بشكل دائم على الخادم.** يتم الاحتفاظ بالملفات التي تم تحميلها في الذاكرة المؤقتة طوال مدة جلسة التحرير، ويتم حذفها تلقائيًا بالكامل عند انتهاء مدة الجلسة (حوالي ساعة واحدة).
- لا يتم تسجيل أي حسابات أو عضويات أو بيانات في قاعدة البيانات.
- عمليات تحليل XML عبر واجهة برمجة التطبيقات (API) محمية بواسطة `defusedxml` (للحماية من هجمات «Billion Laughs»).

## 🧪 نظام الاختبار (CI)

يتميز المشروع بهيكلية اختبار **Round-Trip (ذهاب وإياب)**.
- باستخدام ملفات اختبار واقعية (fixtures)، يتم اختبار أن أكواد المحرك المعطلة أو المعدلة لا تفسد الهياكل الأصلية لقاعدة بيانات التلفزيون.
- في كل عملية `push` و`PR`، يتم تشغيل `tests/test_roundtrip.py` تلقائيًا على GitHub Actions.

## 🌍 دعم اللغات

تتوفر الواجهة ودلائل الاستخدام **بـ 11 لغة**: التركية، الإنجليزية، الألمانية، الروسية، الإسبانية، الإيطالية، الفرنسية، العربية، الفارسية، الأذربيجانية، والبرتغالية.

## 🏗️ بنية المشروع

```
├── app.py # خادم Flask ومسارات API وi18n
├── scm_core.py # محرك Samsung SCM
├── tizen_core.py # محرك Samsung Tizen SQLite
├── lg_core.py # محرك LG XML
├── sony_core.py # محرك XML الخاص بـ Sony
├── hisense_core.py     # محرك SQLite الخاص بـ Hisense
├── templates/ # واجهات HTML باستخدام Jinja2 (11 لغة)
├── static/ # CSS، JS، مخططات YAML لـ OpenAPI
└── tests/
    ├── test_roundtrip.py  # اختبارات ذهاب وإياب لجميع المحركات
    └── fixtures/ # أمثلة قاعدة بيانات تلفزيون حقيقية للاختبارات
```

## 🙏 شكرًا

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — مصدر الإلهام الأول
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — مرجع الهندسة العكسية لتنسيقات العلامات التجارية المتعددة
- **[Türksat Uydu](https://uydu.turksat.com.tr/)** — قاعدة بيانات ترددات Türksat

## 📄 الترخيص

تم توفيره كمصدر مفتوح بموجب ترخيص MIT.
> "Samsung" و"LG" و"Sony" و"Hisense" و"Panasonic" وشعاراتها هي علامات تجارية مسجلة للشركات المعنية. هذا أداة مجتمعية مستقلة ومفتوحة المصدر.

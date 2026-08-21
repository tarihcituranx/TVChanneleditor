[🇹🇷 TR](README.md) | [🇺🇸 EN](README_en.md) | [🇩🇪 DE](README_de.md) | [🇷🇺 RU](README_ru.md) | [🇪🇸 ES](README_es.md) | [🇮🇹 IT](README_it.md) | [🇫🇷 FR](README_fr.md) | [🇸🇦 AR](README_ar.md) | [🇮🇷 FA](README_fa.md) | [🇦🇿 AZ](README_az.md) | [🇵🇹 PT](README_pt.md)

**Última actualización:** 21/08/2026

# 📺 Editor de canales de televisión

> **Editor de listas de canales de televisión multimarca** — Edita tus listas de canales de televisión de Samsung, LG, Sony y Hisense a través del navegador.

[![Demostración en directo](https://img.shields.io/badge/🌐_Canlı_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![Documentación de la API](https://img.shields.io/badge/API-Swagger_UI-orange)](https://tvchanneleditor.onrender.com/api/docs)
[![CI](https://github.com/tarihcituranx/TVChanneleditor/actions/workflows/test.yml/badge.svg)](https://github.com/tarihcituranx/TVChanneleditor/actions)
[![Licencia: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENCIA)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org)

---

## ✨ ¿Para qué sirve?

Es una herramienta de código abierto que te permite editar visualmente, mediante la función **arrastrar y soltar** en tu navegador, el archivo de la lista de canales que tu televisor transfiere a una memoria USB. No requiere instalación, funciona directamente desde el navegador o a través de la API REST.

## 👤 ¿Quién puede utilizarlo?

- Quienes deseen editar la lista de canales de un televisor Samsung desde el ordenador
- Quienes deseen editar archivos XML `.tll` de LG GlobalClone
- Quienes trabajen con listas `sdb.xml` de Sony y `servicelist.db` de Hisense
- Desarrolladores que deseen modificar la lista de canales de forma programática
- Quienes deseen automatizar la lista de canales mediante un agente de IA

## 📺 Formatos compatibles (matriz de compatibilidad)

| Formato | Lectura | Edición | Reconstrucción | Nota |
|--------|:---:|:---:|:---:|-----|
| **Samsung `.scm`** | ✅ | ✅ | ✅ | Series E/F/H (binario) |
| **Samsung Tizen `.zip`** | ✅ | ✅ | ✅ | Series J/K/M/Q/R/T (SQLite) |
| **Sony `sdb.xml`** | ✅ | ✅ | ✅ | Serie BRAVIA |
| **Hisense `servicelist.db`** | ✅ | ✅ | ✅ | Modelos de 2017 y 2021 |
| **LG XML `.tll`** | ✅ | ✅ | ✅ | Solo GlobalClone XML (no compatible con binario) |
| **Panasonic `svl.*`** | 🔜 | 🔜 | 🔜 | Programado / En fase de desarrollo |

> **⚠️ Nota importante sobre la compatibilidad con LG:** No se admiten los archivos **binarios .tll** de la generación anterior de LG. Solo se pueden procesar los archivos `.tll` de nueva generación basados en XML (GlobalClone). Para los archivos antiguos, debes utilizar la aplicación de escritorio *ChanSort*.


## ⚠️ Restricciones importantes

Antes de utilizarlo, ten en cuenta las siguientes limitaciones técnicas:
- **LG Binary TLL:** No se admiten los archivos binarios `.tll` de la generación anterior.
- **Panasonic SVL:** La compatibilidad se encuentra en fase de desarrollo (prevista).
- **Verificación de frecuencia:** Solo está activa para los datos del satélite Türksat.
- **Límite de tamaño de archivo:** Los archivos cargados pueden tener un tamaño máximo de **2 MB**.
- **Sesión temporal:** Los archivos no se almacenan de forma permanente, sino que se borran automáticamente al finalizar la sesión.

## 🚀 Inicio rápido

1. **Transferir del televisor a un USB:** Desde el menú del televisor (Emisión > Ajustes avanzados), transfiere la lista de canales a un USB con formato FAT32.
2. **Subir:** Arrastra y suelta el archivo del USB en la página web.
3. **Edita:** Ordena los elementos arrastrando y soltando, elimina los que no necesites o utiliza 💡 las plantillas inteligentes.
4. **Descarga:** Vuelve a descargar el archivo editado a tu ordenador.
5. **Instálalo en el televisor:** vuelve a conectar la memoria USB al televisor e importa la nueva lista.

## 🛰️ Compatibilidad con satélites y frecuencias

Las listas de canales **DVB-S/S2** se pueden procesar sin problemas en cuanto al formato. **La función de verificación automática de frecuencias (detección de frecuencias antiguas o erróneas) solo está activa actualmente para los datos de Türksat 4A/5B.** Los demás satélites (Hotbird, Astra, etc.) son totalmente compatibles para la clasificación y la edición.

---

## 🔌 ¿Cómo funciona la API para desarrolladores (REST)?

Existe un sencillo flujo de tres pasos para los agentes de IA y los desarrolladores. Para obtener más detalles, puedes consultar los enlaces a [Swagger UI](https://tvchanneleditor.onrender.com/api/docs) o al [esquema OpenAPI](https://tvchanneleditor.onrender.com/api/openapi.txt).

**Paso 1: Carga (Upload)**
```http
POST /upload
Content-Type: multipart/form-data
```
*(Devuelve como respuesta un `session_id` y una lista JSON de los canales)*

**Paso 2: Creación (Build)**
```http
POST /build
Content-Type: application/json
{
  "session_id": "uuid-...",
  "channels": [ ... lista editada ... ]
}
```
*(Devuelve como respuesta el enlace `/download/...` desde el que se puede descargar el archivo)*

**Paso 3: Descarga (Download)**
```http
GET /download/{session_id}/{filename}
```
*(Se descarga el archivo binario o comprimido editado)*

## 🔐 Privacidad y seguridad

- Hay un límite de tamaño de archivo de **2 MB**.
- **Los archivos no se almacenan de forma permanente en el servidor.** Los archivos subidos se procesan en el almacenamiento temporal del servidor durante la sesión de edición, no se archivan de forma permanente y se eliminan por completo de forma automática cuando expira la sesión (aproximadamente 1 hora).
- No hay registros de cuentas, suscripciones ni bases de datos.
- Las operaciones de análisis de XML en la API (contra ataques «Billion Laughs») están protegidas con `defusedxml`.

## 🧪 Sistema de pruebas (CI)

El proyecto cuenta con una arquitectura de pruebas **Round-Trip (ida y vuelta)**.
- Mediante el uso de archivos de prueba del mundo real (fixtures), se comprueba que el código del motor, aunque se haya dañado o modificado, no altere las estructuras originales de la base de datos de televisión.
- En cada operación de `push` y `PR`, el archivo `tests/test_roundtrip.py` se ejecuta automáticamente en GitHub Actions.

## 🌍 Compatibilidad lingüística

La interfaz y las guías de uso están disponibles en **11 idiomas**: turco, inglés, alemán, ruso, español, italiano, francés, árabe, persa, azerbaiyano y portugués.

## 🏗️ Estructura del proyecto

```
├── app.py # Servidor Flask, rutas de la API e i18n
├── scm_core.py # Motor SCM de Samsung
├── tizen_core.py # Motor SQLite de Samsung Tizen
├── lg_core.py # Motor XML de LG
├── sony_core.py # Motor XML de Sony
├── hisense_core.py     # Motor SQLite de Hisense
├── templates/ # Interfaces HTML de Jinja2 (11 idiomas)
├── static/ # CSS, JS, esquemas YAML de OpenAPI
└── tests/
    ├── test_roundtrip.py  # Pruebas de ida y vuelta para todos los motores
    └── fixtures/ # Ejemplos de bases de datos de televisores reales para las pruebas
```

## 🙏 Gracias

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — Fuente de inspiración inicial
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — Referencia de ingeniería inversa para formatos de múltiples marcas
- **[Türksat Uydu](https://uydu.turksat.com.tr/)** — Base de datos de frecuencias de Türksat

## 📄 Licencia

Se ofrece como código abierto bajo la licencia MIT.
> «Samsung», «LG», «Sony», «Hisense», «Panasonic» y sus logotipos son marcas registradas de sus respectivas empresas. Esta es una herramienta comunitaria independiente y de código abierto.

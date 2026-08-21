**Última actualización:** 21/08/2026

# 📺 Editor de canales de televisión

> **Editor de listas de canales de televisión multimarca** — Una única plataforma para Samsung, LG, Sony, Hisense y muchas más marcas.

[![Demostración en directo](https://img.shields.io/badge/🌐_Canlı_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![Licencia: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue)](https://python.org)

---

## 🎯 ¿Qué hace?

Puedes editar visualmente en el navegador, mediante **arrastrar y soltar**, el archivo de la lista de canales que tu televisor ha transferido al USB y volver a cargarlo en el televisor. **Los datos solo se almacenan de forma temporal (en RAM/Temp) durante el proceso; no se guardan de forma permanente.**

---

## 📺 Marcas de televisores compatibles

| Marca | Formato | Estado |
|-------|--------|-------|
| **Samsung** (series E/F/H) | `.scm` | ✅ Compatibilidad total |
| **Samsung** (J/K/M/Q/R/T - Tizen) | `.zip` (SQLite) | ✅ Compatibilidad total |
| **LG** (webOS 5+) | `.tll` (XML) | ✅ Compatibilidad total |
| **Sony BRAVIA** | `sdb.xml` | ✅ Compatibilidad total |
| **Hisense** (2017+) | `servicelist.db` | ✅ Compatibilidad total |
| **Panasonic VIERA** | `svl.db / svl.bin` | 🔄 Beta |
| Philips, Toshiba, Grundig... | `*.db / *.xml` | 🔜 Próximamente |

## 🛰️ Satélites compatibles

**Türksat 4A/5B** · **Hotbird 13E** · **Astra 19.2E** · y todos los demás satélites DVB-S

---

## ✨ Características

- **🪄 Varita mágica** — Aplica plantillas de «General», «Noticias» y «Deportes» con un solo clic
- **🛠️ Creador de plantillas** — Crea y guarda tu propia lista ideal
- **📱 Transferencia al dispositivo mediante código** — Transfiere fácilmente la lista de canales desde el móvil que tienes junto al televisor al ordenador con un código de 8 caracteres
- **🔍 Verificación automática de frecuencias** — Detecta automáticamente frecuencias antiguas o erróneas (Türksat)
- **⭐ Favoritos y bloqueo** — Configuración de favoritos (1-5) y bloqueo infantil
- **🗑️ Acciones masivas** — Elimina de forma masiva canales encriptados, emisoras de radio o elementos seleccionados
- **🌙 Tema oscuro/claro y 👁️ Modo para daltónicos** — Interfaz accesible para todos
- **🌐 11 idiomas disponibles** — Compatible con turco e inglés
- **📊 Privacidad total (análisis sin cookies)** — Estadísticas integradas que no utilizan cookies ni datos personales
- **📱 Totalmente adaptable** — Compatible con ordenador, tableta y móvil

---

## 🚀 Uso en vivo

Úsalo directamente en el navegador sin necesidad de instalación:

👉 **[tvchanneleditor.onrender.com](https://tvchanneleditor.onrender.com)**

---

## 💻 Instalación local

```bash
git clone https://github.com/tarihcituranx/TVChanneleditor.git
cd TVChanneleditor
pip install -r requirements.txt
python3 app.py
```

Ve a la dirección `http://127.0.0.1:5000` en el navegador.

---

## 🏗️ Estructura del proyecto

```
├── app.py # Aplicación principal de Flask y encabezados de seguridad
├── scm_core.py # Motor SCM (binario) de Samsung
├── tizen_core.py # Motor SQLite de Samsung Tizen
├── lg_core.py # Motor XML de LG GlobalClone
├── sony_core.py # Motor sdb.xml de Sony
├── hisense_core.py     # Motor SQLite de Hisense
├── templates/ # Plantillas HTML de Jinja2 (11 idiomas)
├── static/
│   ├── css/style.css   # Tema oscuro/claro + todos los estilos
│   ├── js/app.js # Frontend (arrastrar y soltar, renderizado de canales, plantilla)
│   └── data/ # frecuencias.json, plantillas.json
```

---

## 🔐 Seguridad

- Todos los encabezados de seguridad están activos (CSP, HSTS, CORP, COOP, Referrer-Policy...)
- Límite de tamaño de archivo: 2 MB
- Los archivos subidos se eliminan tras su procesamiento
- No se registra ningún dato de los canales en el servidor
- Contacto de seguridad: `tarihcituranx@proton.me`

---

## 🤖 Guía de inteligencia artificial

Si estás desarrollando con el asistente de IA, lee el archivo [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md).

---

## 🔌 Uso de la API para desarrolladores y los agentes de IA (Developer API)

Este proyecto no es solo un sitio web, sino que también está diseñado como una **API REST** completa que los agentes de IA (AI Agents) y los desarrolladores pueden utilizar directamente mediante código.

> 🧑‍💻 **Para desarrolladores:** Puedes consultar la documentación interactiva de Swagger UI en [tvchanneleditor.onrender.com/api/docs](https://tvchanneleditor.onrender.com/api/docs).
> 
> 🤖 **Para agentes de IA (ChatGPT, Claude, etc.):** Podéis proporcionar a la IA el esquema OpenAPI en texto plano (Plain-Text), legible por máquina, a través de este enlace: [tvchanneleditor.onrender.com/api/openapi.txt](https://tvchanneleditor.onrender.com/api/openapi.txt)


Para que esto funcione, debes añadir las claves autorizadas a las variables de entorno del servidor (o de tu ordenador):
```bash
```

### 4. Comprobación de la versión y la implementación (Version Check)
Para comprobar en cuestión de segundos si el servidor de renderizado ha publicado el último commit de GitHub o si sigue en la caché:
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

## 🙏 Gracias

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — Primera fuente de inspiración
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — Referencia de ingeniería inversa para SCM y formatos multimarca
- **[Satélite Türksat](https://uydu.turksat.com.tr/)** — Base de datos de verificación de frecuencias de Türksat

---

## 📄 Licencia

Se ofrece como código abierto bajo la licencia MIT.

> «Samsung», «LG», «Sony», «Hisense», «Panasonic» y sus logotipos son marcas registradas de las empresas correspondientes. Se trata de una herramienta comunitaria independiente y de código abierto.

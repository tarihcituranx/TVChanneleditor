[🇹🇷 TR](README.md) | [🇺🇸 EN](README_en.md) | [🇩🇪 DE](README_de.md) | [🇷🇺 RU](README_ru.md) | [🇪🇸 ES](README_es.md) | [🇮🇹 IT](README_it.md) | [🇫🇷 FR](README_fr.md) | [🇸🇦 AR](README_ar.md) | [🇮🇷 FA](README_fa.md) | [🇦🇿 AZ](README_az.md) | [🇵🇹 PT](README_pt.md)

**Dernière mise à jour :** 21/08/2026

# 📺 Éditeur de chaînes TV

> **Éditeur de listes de chaînes TV multimarques** — Une plateforme unique pour Samsung, LG, Sony, Hisense et bien d'autres.

[![Démonstration en direct](https://img.shields.io/badge/🌐_Canlı_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![CI](https://github.com/tarihcituranx/TVChanneleditor/actions/workflows/test.yml/badge.svg)](https://github.com/tarihcituranx/TVChanneleditor/actions)
[![Licence : MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org)
[![Documentation de l'API](https://img.shields.io/badge/API-Swagger_UI-orange)](https://tvchanneleditor.onrender.com/api/docs)

---

## 🎯 À quoi ça sert ?

Vous pouvez modifier visuellement le fichier de liste des chaînes que votre téléviseur a transféré sur le port USB à l'aide de la fonction **glisser-déposer** dans votre navigateur, puis le réimporter sur votre téléviseur. **Les données ne sont conservées que temporairement (RAM/Temp) pendant le traitement et ne sont pas stockées de manière permanente.**

---

## 📺 Marques de téléviseurs prises en charge

| Marque | Format | Statut |
|-------|--------|-------|
| **Samsung** (séries E/F/H) | `.scm` | ✅ Prise en charge complète |
| **Samsung** (J/K/M/Q/R/T - Tizen) | `.zip` (SQLite) | ✅ Prise en charge complète |
| **LG** (webOS 5+) | `.tll` (XML) | ✅ Prise en charge complète |
| **Sony BRAVIA** | `sdb.xml` | ✅ Prise en charge complète |
| **Hisense** (2017+) | `servicelist.db` | ✅ Prise en charge complète |
| **Panasonic VIERA** | `svl.db / svl.bin` | 🔄 Bêta |
| Philips, Toshiba, Grundig... | `*.db / *.xml` | 🔜 Bientôt disponible |

## 🛰️ Satellites pris en charge

**Türksat 4A/5B** · **Hotbird 13E** · **Astra 19,2E** · et tous les autres satellites DVB-S

---

## ✨ Fonctionnalités

- **💡 Modèles intelligents** — Appliquez les modèles Général / Actualités / Sport en un seul clic
- **🛠️ Créateur de modèles** — Créez et enregistrez votre liste idéale
- **📱 Transfert vers l'appareil via un code** — Transférez facilement la liste des chaînes de votre téléphone portable vers votre ordinateur à l'aide d'un code à 8 caractères
- **🔍 Vérification automatique des fréquences** — Détecte automatiquement les fréquences obsolètes ou erronées (Türksat)
- **⭐ Favoris & Verrouillage** — Gestion des favoris (1 à 5) et du verrouillage parental
- **🗑️ Opérations groupées** — Supprimez en masse les chaînes cryptées, les stations de radio ou les éléments sélectionnés
- **🌙 Thème sombre/clair & 👁️ Mode daltonisme** — Une interface accessible à tous
- **🌐 Prise en charge de 11 langues**
- **📊 Confidentialité totale (analyses sans cookies)** — Statistiques intégrées n’utilisant ni cookies ni données personnelles
- **📱 Entièrement responsive** — Compatible avec les ordinateurs de bureau, les tablettes et les mobiles

---

## 🚀 Utilisation en ligne

Utilisez-le directement dans votre navigateur, sans aucune installation :

👉 **[tvchanneleditor.onrender.com](https://tvchanneleditor.onrender.com)**

---

## 💻 Installation locale

```bash
git clone https://github.com/tarihcituranx/TVChanneleditor.git
cd TVChanneleditor
pip install -r requirements.txt
python3 app.py
```

Rendez-vous à l’adresse `http://127.0.0.1:5000` dans votre navigateur.

---

## 🏗️ Structure du projet

```
├── app.py # Application principale Flask et en-têtes de sécurité
├── scm_core.py # Moteur Samsung SCM (binaire)
├── tizen_core.py # Moteur SQLite Samsung Tizen
├── lg_core.py # Moteur XML LG GlobalClone
├── sony_core.py # Moteur sdb.xml de Sony
├── hisense_core.py     # Moteur SQLite de Hisense
├── templates/ # Modèles HTML Jinja2 (11 langues)
├── static/
│   ├── css/style.css   # Thème sombre/clair + tous les styles
│   ├── js/app.js # Front-end (glisser-déposer, rendu des chaînes, modèle)
│   └── data/ # frekanslar.json, templates.json
```

---

## 🔐 Sécurité

- Tous les en-têtes de sécurité sont activés (CSP, HSTS, CORP, COOP, Referrer-Policy...)
- Limite de taille des fichiers : 2 Mo
- Les fichiers téléchargés sont supprimés après leur traitement
- Aucune donnée de canal n’est enregistrée sur le serveur
- Contact sécurité : `tarihcituranx@proton.me`

---

## 🤖 Guide de l’IA

Si vous développez avec l’assistant IA, consultez le fichier [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md).

---

## 🔌 Utilisation de l’API développeur et des agents IA (Developer API)

Ce projet n’est pas seulement un site web, mais aussi une **API REST** à part entière, conçue pour être utilisée directement par les agents IA (AI Agents) et les développeurs via leur code.

> 🧑‍💻 **Pour les développeurs :** vous pouvez consulter la documentation interactive Swagger UI à l'adresse [tvchanneleditor.onrender.com/api/docs](https://tvchanneleditor.onrender.com/api/docs).
> 
> 🤖 **Pour les agents IA (ChatGPT, Claude, etc.) :** Vous pouvez fournir à l’IA le schéma OpenAPI au format texte brut (plain-text) lisible par machine via ce lien : [tvchanneleditor.onrender.com/api/openapi.txt](https://tvchanneleditor.onrender.com/api/openapi.txt)



### Vérification de la version et du déploiement (Version Check)
Pour vérifier en une seconde si le dernier commit GitHub du serveur de rendu a bien été mis en production ou s’il est resté en cache :
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

## 🙏 Remerciements

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — Première source d'inspiration
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — Référence de rétro-ingénierie pour SCM et les formats multimarques
- **[Türksat Satellite](https://uydu.turksat.com.tr/)** — Base de données de vérification des fréquences Türksat

---

## 📄 Licence

Distribué en open source sous licence MIT.

> « Samsung », « LG », « Sony », « Hisense », « Panasonic » et leurs logos sont des marques déposées des sociétés concernées. Il s'agit d'un outil communautaire indépendant et open source.

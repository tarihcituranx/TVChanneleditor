[🇹🇷 TR](README.md) | [🇺🇸 EN](README_en.md) | [🇩🇪 DE](README_de.md) | [🇷🇺 RU](README_ru.md) | [🇪🇸 ES](README_es.md) | [🇮🇹 IT](README_it.md) | [🇫🇷 FR](README_fr.md) | [🇸🇦 AR](README_ar.md) | [🇮🇷 FA](README_fa.md) | [🇦🇿 AZ](README_az.md) | [🇵🇹 PT](README_pt.md)

**Dernière mise à jour :** 21/08/2026

# 📺 Éditeur de chaînes TV

> **Éditeur de listes de chaînes TV multimarques** — Modifiez vos listes de chaînes TV Samsung, LG, Sony et Hisense depuis votre navigateur.

[![Démonstration en direct](https://img.shields.io/badge/🌐_Canlı_Demo-tvchanneleditor.onrender.com-blue)](https://tvchanneleditor.onrender.com)
[![Documentation de l'API](https://img.shields.io/badge/API-Swagger_UI-orange)](https://tvchanneleditor.onrender.com/api/docs)
[![CI](https://github.com/tarihcituranx/TVChanneleditor/actions/workflows/test.yml/badge.svg)](https://github.com/tarihcituranx/TVChanneleditor/actions)
[![Licence : MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENCE)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org)

---

## ✨ À quoi ça sert ?

Il s'agit d'un outil open source qui vous permet de modifier visuellement, via la méthode **glisser-déposer** dans votre navigateur, le fichier de liste de chaînes que votre téléviseur a transféré sur une clé USB. Il ne nécessite aucune installation et fonctionne directement depuis le navigateur ou via l'API REST.

## 📺 Formats pris en charge (tableau de compatibilité)

| Format | Lecture | Édition | Recréation | Remarque |
|--------|:---:|:---:|:---:|-----|
| **Samsung `.scm`** | ✅ | ✅ | ✅ | Séries E/F/H (binaire) |
| **Samsung Tizen `.zip`** | ✅ | ✅ | ✅ | Séries J/K/M/Q/R/T (SQLite) |
| **Sony `sdb.xml`** | ✅ | ✅ | ✅ | Série BRAVIA |
| **Hisense `servicelist.db`** | ✅ | ✅ | ✅ | Modèles 2017 et 2021 |
| **LG XML `.tll`** | ✅ | ✅ | ✅ | Uniquement GlobalClone XML (le format binaire n'est pas pris en charge) |
| **Panasonic `svl.*`** | 🔜 | 🔜 | 🔜 | Prévu / En cours de développement |

> **⚠️ Remarque importante concernant la compatibilité LG :** Les fichiers **binaires .tll** de l'ancienne génération de LG ne sont pas pris en charge. Seuls les fichiers `.tll` de nouvelle génération basés sur XML (GlobalClone) peuvent être traités. Pour les anciens fichiers, vous devez utiliser l’application de bureau *ChanSort*.

## 🚀 Démarrage rapide

1. **Transférez depuis le téléviseur vers une clé USB :** depuis le menu du téléviseur (Diffusion > Paramètres avancés), transférez la liste des chaînes vers une clé USB formatée en FAT32.
2. **Importez :** glissez-déposez le fichier de la clé USB sur le site.
3. **Modifier :** Triez par glisser-déposer, supprimez les éléments inutiles ou utilisez les 💡 modèles intelligents.
4. **Télécharger :** Téléchargez le fichier modifié sur votre ordinateur.
5. **Importez sur votre téléviseur :** reconnectez la clé USB à votre téléviseur et importez la nouvelle liste.

## 🛰️ Prise en charge des satellites et des fréquences

Les listes de chaînes au format **DVB-S/S2** peuvent être traitées sans problème. **La fonctionnalité de vérification automatique des fréquences (détection des fréquences obsolètes/erronées) n’est actuellement active que pour les données Türksat 4A/5B.** Les autres satellites (Hotbird, Astra, etc.) sont entièrement pris en charge pour le tri et l’édition.

---

## 🔌 Comment fonctionne l’API pour développeurs (REST) ?

Un processus simple en 3 étapes est disponible pour les agents IA et les développeurs. Pour plus de détails, vous pouvez consulter les liens [Swagger UI](https://tvchanneleditor.onrender.com/api/docs) ou [schéma OpenAPI](https://tvchanneleditor.onrender.com/api/openapi.txt).

**Étape 1 : Téléchargement (Upload)**
```http
POST /upload
Content-Type: multipart/form-data
```
*(Renvoie en réponse un `session_id` et une liste JSON des canaux)*

**Étape 2 : Compilation (Build)**
```http
POST /build
Content-Type: application/json
{
  "session_id": "uuid-...",
  "channels": [ ... liste formatée ... ]
}
```
*(La réponse renvoie un lien `/download/...` permettant de télécharger le fichier)*

**Étape 3 : Téléchargement (Download)**
```http
GET /download/{session_id}/{filename}
```
*(Le fichier binaire/archivé modifié est téléchargé)*

## 🔐 Confidentialité et sécurité

- La taille des fichiers est limitée à **2 Mo**.
- **Les fichiers ne sont pas stockés de manière permanente sur le serveur.** Les fichiers téléchargés sont conservés en mémoire temporaire pendant la durée de la session d’édition et sont automatiquement et intégralement supprimés à l’expiration de la session (environ 1 heure).
- Il n’y a aucune création de compte, d’abonnement ni de journalisation dans la base de données.
- Les opérations de parsing XML sur l’API (contre les attaques « Billion Laughs ») sont protégées par `defusedxml`.

## 🧪 Système de test (CI)

Le projet dispose d’une architecture de test **Round-Trip (aller-retour)**.
- À l’aide de fichiers de test (fixtures) issus du monde réel, on vérifie que les codes du moteur corrompus ou modifiés n’altèrent pas les structures d’origine de la base de données TV.
- À chaque opération `push` et `PR`, le script `tests/test_roundtrip.py` s’exécute automatiquement sur GitHub Actions.

## 🌍 Prise en charge linguistique

L'interface et les guides d'utilisation sont disponibles **en 11 langues** : turc, anglais, allemand, russe, espagnol, italien, français, arabe, persan, azéri et portugais.

## 🏗️ Structure du projet

```
├── app.py # Serveur Flask, routes API et i18n
├── scm_core.py # Moteur SCM Samsung
├── tizen_core.py # Moteur SQLite Samsung Tizen
├── lg_core.py # Moteur XML LG
├── sony_core.py # Moteur XML Sony
├── hisense_core.py     # Moteur SQLite Hisense
├── templates/ # Interfaces HTML Jinja2 (11 langues)
├── static/ # CSS, JS, schémas YAML OpenAPI
└── tests/
    ├── test_roundtrip.py  # Tests aller-retour pour tous les moteurs
    └── fixtures/ # Exemples de bases de données TV réelles pour les tests
```

## 🙏 Remerciements

- **[İltekin/scm-editor](https://github.com/iltekin/scm-editor)** — Première source d’inspiration
- **[PredatH0r/ChanSort](https://github.com/PredatH0r/ChanSort)** — Référence de rétro-ingénierie pour les formats multimarques
- **[Türksat Satellite](https://uydu.turksat.com.tr/)** — Base de données des fréquences Türksat

## 📄 Licence

Distribué en open source sous licence MIT.
> « Samsung », « LG », « Sony », « Hisense », « Panasonic » et leurs logos sont des marques déposées des sociétés respectives. Il s'agit d'un outil communautaire indépendant et open source.

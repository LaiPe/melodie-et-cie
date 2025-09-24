
# Mélodie & Cie – Maquette de site vitrine

Mélodie & Cie est la maquette d’un site vitrine imaginé pour une entreprise fictive spécialisée dans la musique. Le site met en avant les services proposés par l'entreprise, c'est à dire la production musicale, l'évènementiel et la formation. La diversité des activités proposées est un choix assumé pour illustrer ma capacité à répondre à des cahiers des charges complexes et à des attentes très différentes.

Le site propose une navigation claire, une expérience responsive et un formulaire de contact pour faciliter les échanges avec les visiteurs. L’ensemble du contenu éditorial, des témoignages aux informations sur les formations et les événements, est entièrement modifiable par l’équipe via une interface d’administration simple et intuitive.

Ce projet met l’accent sur l’autonomie des utilisateurs, la valorisation de l’expertise musicale et la facilité d’évolution du site au fil du temps.

## 🚀 Installation rapide

```bash
npm install
```

## 🛠️ Lancer le projet en développement

```bash
npm run dev
```

Le site sera accessible à l'adresse : http://localhost:8080

## 🧪 Tests automatisés

Le projet inclut une suite de tests E2E (End-to-End) pour vérifier le bon fonctionnement du site et du back-office CMS.

### Lancement des tests (recommandé)

```bash
npm test
```

Cette commande :
- ✅ Vérifie et crée automatiquement l'environnement virtuel Python si nécessaire
- ✅ Installe automatiquement les dépendances Python manquantes
- ✅ Lance tous les tests (navigation + back-office CMS)
- ✅ Fonctionne sur Windows, macOS et Linux

### Lancement direct (si l'environnement est déjà configuré)

```bash
npm run test:direct
```

### Tests inclus

1. **Test de navigation interne** : Vérifie tous les liens du site
2. **Test back-office CMS** : Test complet de création/modification/suppression de contenu

> **Note** : Les tests nécessitent que le serveur de développement soit lancé (`npm run dev`) dans un autre terminal.


## 🏗️ Générer le site pour la production

```bash
npm run build
```

Les fichiers générés seront dans le dossier `_site/`.

## 📁 Structure du projet

```
├── src/
│   ├── index.njk                # Page d'accueil (template Nunjucks)
│   ├── index.11tydata.json      # Données dynamiques de la page d'accueil
│   ├── services/                # Datas et templates (formations, production, etc.)
│   ├── admin/                   # Décap CMS (Netlify CMS)
│   └── _includes/               # Composants et layouts Nunjucks
├── _site/                       # Fichiers générés
├── .eleventy.js                 # Configuration Eleventy
└── package.json                 # Dépendances et scripts
```

## ✨ Fonctionnalités principales

Le site propose un design responsive, une navigation intuitive et des sections bien structurées (services, témoignages, staff, FAQ, etc.).
Tout le contenu éditorial est modifiable via Decap CMS (Netlify CMS), permettant à l’équipe de gérer facilement les textes, listes, images et collections sans intervention technique.

Les données sont organisées de façon atomique (un fichier JSON par élément éditable), ce qui facilite la maintenance, l’édition et l’évolution du site.

## ⚙️ Technologies utilisées

- **Eleventy (11ty)** : Générateur de site statique moderne, rapide et flexible
- **Nunjucks** : Moteur de templates pour la génération dynamique des pages
- **Decap CMS (Netlify CMS)** : Interface d’administration pour la gestion du contenu par l’équipe
- **JSON** : Structuration claire et modulaire des données éditoriales
- **Netlify** : Hébergement, déploiement continu et gestion des redirections

## 📱 Compatibilité

- Navigateurs modernes (Chrome, Firefox, Safari, Edge)
- Responsive design pour mobile, tablette et desktop
- Accessibilité optimisée

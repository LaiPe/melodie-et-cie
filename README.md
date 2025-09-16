
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
│   ├── services/                # Données atomiques (formations, production, etc.)
│   ├── staff/                   # Membres du staff (JSON)
│   └── _includes/               # Composants et layouts Nunjucks
├── _site/                       # Fichiers générés
├── .eleventy.js                 # Configuration Eleventy
├── package.json                 # Dépendances et scripts
└── src/admin/                   # Décap CMS (Netlify CMS)
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
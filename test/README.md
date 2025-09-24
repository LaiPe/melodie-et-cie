# Tests E2E pour Mélodie & Cie

Ce dossier contient une suite de tests end-to-end automatisés qui vérifient le bon fonctionnement du site et du back-office CMS.

## 🚀 Démarrage rapide

### Pour nouveaux utilisateurs (recommandé)
```bash
# Depuis la racine du projet
npm test
```
Cette commande fait **tout automatiquement** :
- ✅ Crée l'environnement virtuel Python si nécessaire
- ✅ Installe toutes les dépendances Python requises
- ✅ Lance la suite complète de tests
- ✅ Fournit un rapport détaillé des résultats

### Si l'environnement est déjà configuré
```bash
# Lancement direct (plus rapide)
npm run test:direct
```

## 📋 Prérequis simples

- **Python 3.7+** installé sur votre système
- **Google Chrome** installé  
- **Serveur de développement actif** : `npm run dev` (dans un autre terminal)

C'est tout ! Les tests s'occupent du reste automatiquement.

## 🧪 Tests inclus

### 1. 🧭 Test de navigation interne
- Vérifie tous les liens du site (Accueil → Services → Formation/Événements/Production/Contact)
- Navigation directe optimisée sans détours inutiles
- Vérification de l'accessibilité et du contenu des pages

### 2. 🎯 Test du back-office CMS  
- Test complet de création de contenu via Decap CMS
- Gestion intelligente des collisions (noms uniques avec timestamp)
- Processus : Création → Vérification → Nettoyage automatique
- Support des emojis avec fallback automatique

## 🎛️ Options de lancement

### Méthode npm (recommandée)
```bash
# Configuration automatique + tous les tests
npm test

# Tests directs (si environnement OK)  
npm run test:direct
```

### Méthode Python directe (pour développeurs)
```bash
# Depuis le dossier test/
python setup-and-test.py     # Configuration auto + tests
python run_all_tests.py      # Tous les tests
python test_navigation_interne.py  # Navigation seule
python test_backoffice_cms.py      # CMS seul
```

## ⚙️ Architecture des tests

### 🛠️ Utilitaires intelligents (`navigation_utils.py`)

**NavigationHelper** - Navigation robuste
- Stratégies multiples pour trouver les éléments
- Gestion automatique des erreurs avec fallback
- Méthodes spécialisées pour chaque section du site

**CMSHelper** - Interaction avec Decap CMS
- Login et gestion des formulaires automatisés
- Gestion spécialisée du dropdown "Publish" (2 étapes)
- Mapping intelligent des champs de formulaire
- Support des emojis avec caractères de remplacement BMP

### 📁 Structure du projet
```
test/
├── setup-and-test.py           # 🎯 Configuration auto + lancement
├── run_all_tests.py            # Orchestrateur principal
├── test_navigation_interne.py  # Tests de navigation
├── test_backoffice_cms.py      # Tests CMS complets
├── navigation_utils.py         # Utilitaires partagés
├── requirements.txt            # Dépendances Python
└── README.md                   # Cette documentation
```

## 🔧 Configuration avancée

### URLs par défaut
- Site : `http://localhost:8080`
- CMS : `http://localhost:8080/admin/`
- Backend : `http://localhost:8081` (decap-server)

### Personnalisation des ports
```python
# Dans les fichiers de test
self.base_url = "http://localhost:VOTRE_PORT"
```

## 🧹 Fonctionnalités intelligentes

### Gestion automatique des collisions
- **Noms uniques** : Timestamp intégré pour éviter les conflits
- **Nettoyage préventif** : Suppression des résidus d'anciens tests
- **Nettoyage post-test** : Suppression automatique des fichiers créés

### Robustesse des tests
- **Attente intelligente** : Surveillance du rechargement Eleventy
- **Fallback emojis** : Remplacement automatique pour ChromeDriver
- **Multi-sélecteurs** : Plusieurs stratégies pour chaque élément
- **Pause inter-tests** : Évite les conflits de ressources

## 🐛 Dépannage

### ❌ Problèmes courants

**Python non trouvé**
```bash
# Windows : Installer depuis python.org
# macOS : brew install python3  
# Linux : sudo apt install python3 python3-venv
```

**Chrome/ChromeDriver introuvable**
- Vérifiez que Chrome est installé et accessible
- Le WebDriver Manager s'occupe automatiquement de ChromeDriver

**Serveur de développement inaccessible**
```bash
# Vérifiez que le serveur tourne
npm run dev
# Testez manuellement : http://localhost:8080
```

**Tests qui échouent**
1. ✅ Serveur dev actif ? → `npm run dev`
2. ✅ Chrome installé ?
3. ✅ Relancer : `npm test`
4. ✅ Tests individuels : `npm run test:direct`

### � Mode debug
```bash
# Pour identifier les problèmes
python test/test_navigation_interne.py  # Test navigation seul
python test/test_backoffice_cms.py      # Test CMS seul
```

## ✅ Workflow recommandé

### Pour nouveaux contributeurs
```bash
# 1. Cloner le projet
git clone [repository]
cd melodie-et-cie

# 2. Installer dépendances JS
npm install

# 3. Lancer le serveur (terminal 1)
npm run dev

# 4. Lancer les tests (terminal 2)
npm test  # 🎯 Tout est automatique !
```

### Pour développement quotidien  
```bash
# Serveur toujours actif
npm run dev

# Tests rapides
npm run test:direct
```

## 🎯 Bonnes pratiques

1. **Toujours utiliser npm test** pour la première fois
2. **Serveur dev obligatoire** avant les tests CMS
3. **Surveiller la console** pour identifier les problèmes
4. **Ne pas interrompre** les tests CMS (nettoyage automatique)
5. **Utiliser test:direct** pour les tests répétés
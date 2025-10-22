# 🤖 Assistant IA Kaizen - Documentation Intelligente

## 📋 Description

Assistant IA développé pour faciliter l'accès à la documentation Kaizen (261 pages). Permet aux utilisateurs de :
- ✅ Poser des questions en langage naturel
- ✅ Obtenir des réponses précises avec références
- ✅ Créer automatiquement des tickets Freshdesk
- ✅ Consulter l'historique des recherches

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
pip install streamlit
```

### Dépendances système (déjà installées sur Linux)

- `pdftotext` (partie de poppler-utils)

## 💻 Lancement de l'application

### Option 1 : Lancement simple

```bash
streamlit run kaizen_assistant.py
```

### Option 2 : Avec configuration personnalisée

```bash
streamlit run kaizen_assistant.py --server.port 8501 --server.address localhost
```

L'application sera accessible à l'adresse : **http://localhost:8501**

## 📚 Structure du projet

```
kaizen_assistant/
│
├── kaizen_assistant.py          # Application principale
├── chat_history.json            # Historique des conversations (créé automatiquement)
├── README.md                    # Ce fichier
└── requirements.txt             # Dépendances Python
```

## 🎯 Fonctionnalités

### 1. Recherche Intelligente
- Pose de questions en langage naturel
- Recherche contextuelle dans les 261 pages du manuel
- Affichage des extraits pertinents
- Références aux sections du manuel

### 2. Création de Tickets Freshdesk
- Génération automatique d'un résumé de recherche
- Inclusion du contexte et des résultats trouvés
- Template pré-rempli pour Freshdesk
- Date et historique de la recherche

### 3. Historique des Recherches
- Sauvegarde automatique de toutes les questions
- Consultation des recherches précédentes
- Statistiques d'utilisation
- Possibilité de revoir les anciennes réponses

### 4. Interface Intuitive
- Design moderne et responsive
- Exemples de questions suggérées
- Feedback utilisateur (utile/pas utile)
- Sidebar avec statistiques et actions

## 📖 Guide d'utilisation

### Étape 1 : Poser une question

1. Tapez votre question dans la zone de texte
2. Cliquez sur "🔍 Rechercher"
3. Consultez la réponse et les références

**Exemples de questions :**
- "Comment créer un devis ?"
- "Qu'est-ce que l'AICI ?"
- "Comment générer une facture ?"
- "Comment créer un contrat de travail ?"

### Étape 2 : Évaluer la réponse

Trois options :
- 👍 **Oui, parfait** : La réponse répond complètement à votre besoin
- 👌 **Partiellement** : La réponse est incomplète
- 👎 **Non** : La réponse ne convient pas

### Étape 3 : Créer un ticket Freshdesk (si nécessaire)

Si l'IA ne trouve pas la réponse :
1. Cliquez sur "🎫 Créer un ticket Freshdesk"
2. Copiez le résumé généré
3. Rendez-vous sur votre portail Freshdesk
4. Créez un nouveau ticket avec le résumé

## 🔧 Configuration Avancée

### Intégration API Freshdesk (optionnel)

Pour activer la création automatique de tickets :

1. Créer un fichier `.env` :
```env
FRESHDESK_DOMAIN=votre-domaine.freshdesk.com
FRESHDESK_API_KEY=votre_clé_api
```

2. Installer la dépendance :
```bash
pip install python-decouple requests
```

3. Modifier le code pour utiliser l'API Freshdesk

### Intégration API Claude (optionnel)

Pour des réponses plus sophistiquées avec Claude :

1. Obtenir une clé API Anthropic
2. Ajouter dans `.env` :
```env
ANTHROPIC_API_KEY=votre_clé_api
```

3. Installer la dépendance :
```bash
pip install anthropic
```

## 📊 Améliorations Futures

### Version 2.0 (prévue)
- [ ] Intégration complète API Freshdesk
- [ ] Recherche sémantique avancée avec embeddings
- [ ] Support multi-langues
- [ ] Export des réponses en PDF
- [ ] Chat en temps réel avec WebSocket

### Version 3.0 (prévue)
- [ ] Intégration avec Claude API pour réponses sophistiquées
- [ ] Système de feedback et amélioration continue
- [ ] Analytics et tableaux de bord d'utilisation
- [ ] Mode hors-ligne avec cache local

## 🐛 Dépannage

### Problème : "Module streamlit not found"
**Solution :**
```bash
pip install streamlit
```

### Problème : "Cannot find PDF file"
**Solution :**
Vérifiez que les fichiers PDF sont au bon emplacement :
- `/mnt/user-data/uploads/Kaizen_-_Manuel_ope_ratoire.pdf`
- `/mnt/user-data/uploads/Documentation_Utilisateur_KAIZEN.pdf`

### Problème : L'application ne démarre pas
**Solution :**
```bash
# Vérifier la version de Python
python --version  # Doit être 3.8+

# Réinstaller les dépendances
pip install --upgrade streamlit
```

## 📞 Support

Pour toute question ou problème :
1. Consultez la documentation Kaizen
2. Créez un ticket via l'application
3. Contactez le support technique

## 📝 Changelog

### Version 1.0 (22/10/2025)
- ✅ Lancement initial
- ✅ Recherche dans le manuel PDF
- ✅ Interface Streamlit
- ✅ Génération de résumés pour tickets Freshdesk
- ✅ Historique des recherches
- ✅ Système de feedback

## 👥 Contributeurs

- **Développeur Principal** : Claude (Anthropic)
- **Client** : Kangourou Kids / Joey Group
- **Document source** : Manuel Opératoire Kaizen (261 pages)

## 📄 Licence

© 2025 Kangourou Kids - Usage interne uniquement

---

**🚀 Prêt à commencer ? Lancez l'application avec :**
```bash
streamlit run kaizen_assistant.py
```

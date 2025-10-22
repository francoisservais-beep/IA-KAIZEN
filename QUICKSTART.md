# 🚀 Guide de Démarrage Rapide - Assistant Kaizen

## Installation en 3 étapes

### 📥 Étape 1 : Télécharger les fichiers

Assurez-vous d'avoir tous les fichiers suivants :

```
assistant-kaizen/
├── kaizen_assistant.py          # Application principale ⭐
├── freshdesk_integration.py     # Module Freshdesk
├── setup.py                     # Script de configuration
├── requirements.txt             # Dépendances
├── README.md                    # Documentation complète
└── QUICKSTART.md               # Ce fichier
```

### ⚙️ Étape 2 : Configuration automatique

Exécutez le script de configuration :

```bash
python setup.py
```

Ce script va :
- ✅ Vérifier Python 3.8+
- ✅ Installer les dépendances manquantes
- ✅ Vérifier les fichiers PDF
- ✅ Configurer Freshdesk (optionnel)
- ✅ Créer le script de lancement

### 🚀 Étape 3 : Lancer l'application

**Option A : Script de lancement (recommandé)**
```bash
./launch_kaizen.sh
```

**Option B : Commande directe**
```bash
streamlit run kaizen_assistant.py
```

L'application s'ouvrira dans votre navigateur : **http://localhost:8501**

---

## 💡 Utilisation de l'Assistant

### 1️⃣ Poser une question

Tapez votre question dans la zone de texte, par exemple :
- "Comment créer un devis ?"
- "Qu'est-ce que l'AICI ?"
- "Comment générer une facture ?"

### 2️⃣ Obtenir une réponse

Cliquez sur **🔍 Rechercher** et l'IA :
- Analyse le manuel Kaizen (261 pages)
- Trouve les sections pertinentes
- Vous donne une réponse avec références

### 3️⃣ Créer un ticket (si besoin)

Si la réponse n'est pas satisfaisante :
1. Cliquez sur **🎫 Créer un ticket Freshdesk**
2. Copiez le résumé généré
3. Collez-le dans Freshdesk

---

## 🔧 Configuration Freshdesk (Optionnel)

Pour activer la création automatique de tickets :

### Méthode 1 : Via le script setup.py
```bash
python setup.py
# Suivez les instructions pour configurer Freshdesk
```

### Méthode 2 : Configuration manuelle

1. Créez un fichier `.env` à la racine :
```bash
touch .env
```

2. Ajoutez votre configuration :
```env
FRESHDESK_DOMAIN=votre-domaine.freshdesk.com
FRESHDESK_API_KEY=votre_clé_api_freshdesk
```

3. Obtenez votre clé API Freshdesk :
   - Connectez-vous à Freshdesk
   - Allez dans **Profil → Paramètres**
   - Section **Clé API**
   - Copiez votre clé

### Test de connexion

```bash
python freshdesk_integration.py
```

---

## 📊 Exemples de Questions

### Questions Commerciales
- "Comment créer un devis mensualisé ?"
- "Quelle est la différence entre devis réel et mensualisé ?"
- "Comment transformer un devis en contrat ?"
- "Comment gérer la prise en charge tiers-payeur ?"

### Questions RH
- "Comment créer un contrat de travail CD2I ?"
- "Comment faire une DPAE ?"
- "Comment gérer les absences ?"
- "Comment générer les bulletins de paie ?"

### Questions Facturation
- "Comment générer une facture ?"
- "Comment créer un ordre de prélèvement SEPA ?"
- "Comment rembourser un dépôt de garantie ?"
- "Comment générer une attestation fiscale ?"

### Questions Planification
- "Comment faire un appariement ?"
- "Comment accéder au planning ?"
- "Qu'est-ce qu'un créneau global vs précis ?"

---

## 🐛 Problèmes Courants

### Problème : "Module not found"
**Solution :**
```bash
pip install streamlit
```

### Problème : "PDF file not found"
**Solution :**
Vérifiez que les PDFs sont dans `/mnt/user-data/uploads/`

### Problème : L'application ne démarre pas
**Solution :**
```bash
# Vérifier Python
python --version

# Réinstaller streamlit
pip install --upgrade streamlit

# Relancer
streamlit run kaizen_assistant.py
```

### Problème : Port 8501 déjà utilisé
**Solution :**
```bash
streamlit run kaizen_assistant.py --server.port 8502
```

---

## 📱 Interface de l'Application

```
┌─────────────────────────────────────────────────────────┐
│  🤖 Assistant IA Kaizen                     [Sidebar]   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  💬 Posez votre question                                │
│  ┌────────────────────────────────────────────────┐    │
│  │ Que voulez-vous savoir sur Kaizen ?            │    │
│  │                                                 │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  [🔍 Rechercher]  [🎫 Créer un ticket Freshdesk]       │
│                                                          │
│  ────────────────────────────────────────────────────   │
│                                                          │
│  ✅ Réponse                                             │
│  ┌────────────────────────────────────────────────┐    │
│  │ D'après le manuel Kaizen...                     │    │
│  │                                                 │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  📍 Références : Section page 45, page 67               │
│                                                          │
│  Cette réponse vous a-t-elle été utile ?                │
│  [👍 Oui] [👌 Partiellement] [👎 Non]                  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Fonctionnalités Principales

| Fonctionnalité | Description | Statut |
|----------------|-------------|---------|
| 🔍 Recherche intelligente | Trouve les infos dans le manuel | ✅ Actif |
| 💡 Réponses contextuelles | Donne des réponses précises | ✅ Actif |
| 📍 Références | Cite les sources du manuel | ✅ Actif |
| 🎫 Tickets Freshdesk | Crée des tickets automatiquement | ⚙️ À configurer |
| 📜 Historique | Sauvegarde les recherches | ✅ Actif |
| 📊 Statistiques | Suivi des questions | ✅ Actif |
| 💡 Suggestions | Exemples de questions | ✅ Actif |
| 👍 Feedback | Évaluer les réponses | ✅ Actif |

---

## 📞 Besoin d'Aide ?

### Documentation
- **README.md** : Documentation complète
- **Ce fichier** : Guide de démarrage rapide

### Support
1. Consultez le manuel Kaizen dans l'application
2. Créez un ticket via l'application
3. Contactez le support technique

---

## ✅ Checklist de Démarrage

- [ ] Python 3.8+ installé
- [ ] Streamlit installé (`pip install streamlit`)
- [ ] Fichiers PDF présents
- [ ] Application lancée (`streamlit run kaizen_assistant.py`)
- [ ] Interface accessible (http://localhost:8501)
- [ ] Première question posée
- [ ] Réponse obtenue
- [ ] (Optionnel) Freshdesk configuré

---

## 🎓 Tutoriel Vidéo (à venir)

Un tutoriel vidéo sera disponible prochainement pour :
- Installer l'application
- Configurer Freshdesk
- Utiliser efficacement l'assistant
- Créer des tickets

---

**🚀 Prêt à commencer ?**

```bash
python setup.py
./launch_kaizen.sh
```

**🌐 Puis ouvrez : http://localhost:8501**

---

*Assistant Kaizen v1.0 - Octobre 2025*
*Développé pour Kangourou Kids*

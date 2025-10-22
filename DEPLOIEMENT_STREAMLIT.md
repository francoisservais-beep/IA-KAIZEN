# 🚀 Déploiement sur Streamlit Cloud - Guide Complet

## ⚠️ PROBLÈME RÉSOLU

Le problème `FileNotFoundError` a été corrigé dans la nouvelle version !

**Changements effectués :**
- ✅ Chemins de fichiers adaptés pour Streamlit Cloud
- ✅ Gestion d'erreur pour l'historique
- ✅ Vérification de l'existence des PDFs
- ✅ Configuration Streamlit optimisée

---

## 📦 Fichiers Nécessaires

Assurez-vous d'avoir ces fichiers dans votre repository GitHub :

```
votre-repo/
├── kaizen_assistant.py          ✅ (VERSION CORRIGÉE)
├── freshdesk_integration.py     ✅
├── requirements.txt             ✅
├── packages.txt                 ✅ NOUVEAU !
├── .streamlit/
│   └── config.toml             ✅ NOUVEAU !
├── Kaizen_-_Manuel_ope_ratoire.pdf  ⚠️ IMPORTANT !
└── README.md
```

---

## 📄 Fichier PDF - TRÈS IMPORTANT ⚠️

**Le PDF doit être dans votre repository GitHub !**

### Option 1 : Upload Direct (Si < 100 MB)
1. Sur GitHub, cliquez sur "Add file" → "Upload files"
2. Uploadez `Kaizen_-_Manuel_ope_ratoire.pdf`
3. Commit

### Option 2 : Git LFS (Si > 100 MB)
```bash
# Installer Git LFS
git lfs install

# Tracker les PDF
git lfs track "*.pdf"

# Commit
git add .gitattributes
git add Kaizen_-_Manuel_ope_ratoire.pdf
git commit -m "Add PDF with Git LFS"
git push
```

### Option 3 : Hébergement Externe
Si le PDF est trop gros, hébergez-le ailleurs et modifiez le code :
```python
# Dans kaizen_assistant.py
self.pdf_path = "https://votre-url.com/manuel.pdf"
```

---

## 🔧 Nouveaux Fichiers Requis

### 1. packages.txt
Créez ce fichier à la racine :
```
poppler-utils
```

Ce fichier permet d'installer `pdftotext` sur Streamlit Cloud.

### 2. .streamlit/config.toml
Créez le dossier `.streamlit/` et ce fichier dedans :
```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

---

## 🚀 Déploiement Étape par Étape

### Étape 1 : Préparer GitHub

1. **Créer un nouveau repository**
   - Allez sur https://github.com
   - Cliquez sur "New repository"
   - Nom : `kaizen-assistant` ou `ia-kaizen`
   - Public ou Private (les deux fonctionnent)

2. **Uploader tous les fichiers**
   ```bash
   # Via l'interface web GitHub :
   # - Cliquez sur "Add file" → "Upload files"
   # - Glissez tous vos fichiers
   # - Commit
   
   # OU via Git :
   git init
   git add .
   git commit -m "Initial commit - Assistant Kaizen"
   git branch -M main
   git remote add origin https://github.com/VOTRE-USERNAME/kaizen-assistant.git
   git push -u origin main
   ```

3. **Vérifier la structure**
   - Assurez-vous que le PDF est bien uploadé
   - Vérifiez que `packages.txt` est à la racine
   - Vérifiez que `.streamlit/config.toml` existe

### Étape 2 : Déployer sur Streamlit Cloud

1. **Allez sur Streamlit Cloud**
   - URL : https://share.streamlit.io
   - Connectez-vous avec GitHub

2. **Créer une nouvelle app**
   - Cliquez sur "New app"
   - Repository : sélectionnez votre repo
   - Branch : `main`
   - Main file path : `kaizen_assistant.py`

3. **Configuration avancée (optionnel)**
   - Cliquez sur "Advanced settings"
   - Python version : 3.11
   - Secrets (si Freshdesk) :
     ```toml
     FRESHDESK_DOMAIN = "votre-domaine.freshdesk.com"
     FRESHDESK_API_KEY = "votre_clé_api"
     ```

4. **Déployer**
   - Cliquez sur "Deploy!"
   - Attendez 2-5 minutes

### Étape 3 : Tester

1. **Accédez à votre app**
   - URL : `https://votre-app.streamlit.app`

2. **Vérifiez que tout fonctionne**
   - Interface se charge ✅
   - PDF est accessible ✅
   - Recherche fonctionne ✅
   - Historique fonctionne ✅

---

## 🐛 Résolution des Problèmes Courants

### Erreur : "FileNotFoundError"
**Solution :** Le PDF n'est pas dans le repository
- Vérifiez que `Kaizen_-_Manuel_ope_ratoire.pdf` est uploadé
- Vérifiez le nom exact du fichier (sensible à la casse)

### Erreur : "pdftotext: command not found"
**Solution :** `packages.txt` manquant
- Créez le fichier `packages.txt` avec `poppler-utils` dedans
- Redeployez l'app

### Erreur : "ModuleNotFoundError: No module named 'streamlit'"
**Solution :** `requirements.txt` incorrect
- Vérifiez que `streamlit>=1.28.0` est dans requirements.txt

### L'app est lente
**Solution :** PDF trop gros
- Compressez le PDF
- Ou utilisez un hébergement externe pour le PDF

### Historique ne se sauvegarde pas
**Solution :** C'est normal sur Streamlit Cloud gratuit
- L'historique est temporaire
- Il se réinitialise à chaque redémarrage
- Pour un historique persistant, utilisez une base de données externe

---

## 📊 Limitations Streamlit Cloud (Gratuit)

| Fonctionnalité | Limitation | Solution |
|----------------|------------|----------|
| Fichiers | 1 GB max | Compresser ou héberger ailleurs |
| RAM | 1 GB | Optimiser le code |
| CPU | Partagé | OK pour usage normal |
| Stockage | Temporaire | Utiliser DB externe pour persistance |
| Apps | 1 app publique | Illimité avec plan payant |

---

## 💡 Optimisations Recommandées

### 1. Compresser le PDF
```bash
# Avec Ghostscript
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
   -dNOPAUSE -dQUIET -dBATCH \
   -sOutputFile=manuel_compresse.pdf Kaizen_-_Manuel_ope_ratoire.pdf
```

### 2. Ajouter un Cache
Dans `kaizen_assistant.py`, ajoutez :
```python
@st.cache_data
def load_pdf_text(pdf_path):
    # Charger et cacher le texte du PDF
    pass
```

### 3. Base de Données pour l'Historique
Utilisez SQLite ou une DB externe pour la persistance.

---

## ✅ Checklist de Déploiement

Avant de déployer, vérifiez :

- [ ] ✅ Tous les fichiers sont sur GitHub
- [ ] ✅ Le PDF est uploadé (ou lien externe configuré)
- [ ] ✅ `packages.txt` existe avec `poppler-utils`
- [ ] ✅ `.streamlit/config.toml` est configuré
- [ ] ✅ `requirements.txt` contient `streamlit`
- [ ] ✅ Le code a été testé localement
- [ ] ✅ Les chemins de fichiers sont corrects
- [ ] ✅ Pas de données sensibles dans le code

---

## 🎉 Félicitations !

Votre Assistant Kaizen devrait maintenant fonctionner sur Streamlit Cloud !

**URL de votre app :** `https://VOTRE-APP.streamlit.app`

### Prochaines Étapes

1. **Testez toutes les fonctionnalités**
2. **Partagez l'URL avec votre équipe**
3. **Configurez Freshdesk (optionnel)**
4. **Surveillez les logs pour les erreurs**

### Support

Si vous rencontrez des problèmes :
1. Consultez les logs dans "Manage app" sur Streamlit Cloud
2. Vérifiez ce guide
3. Consultez https://docs.streamlit.io

---

**🚀 Bon déploiement !**

# 🚀 Guide de Déploiement - Site Maalem

Ce guide vous aidera à rendre votre site accessible publiquement sur Internet.

## 📋 Table des Matières

1. [Option 1: Déploiement Gratuit (Vercel + Render)](#option-1-déploiement-gratuit)
2. [Option 2: Réseau Local](#option-2-réseau-local)
3. [Option 3: Tunnel ngrok (Temporaire)](#option-3-tunnel-ngrok)

---

## Option 1: Déploiement Gratuit (RECOMMANDÉ) 🎯

### Prérequis
- Compte GitHub (gratuit)
- Compte Vercel (gratuit)
- Compte Render (gratuit)

### Étape 1: Préparer le Code

#### 1.1 Créer un dépôt GitHub

```bash
# Dans le dossier racine du projet
cd "c:\Users\Igolan\Desktop\site maalem"

# Initialiser Git (si pas déjà fait)
git init

# Créer .gitignore
echo "node_modules/
__pycache__/
*.pyc
.env
*.log
dist/
build/
.DS_Store
media/
staticfiles/" > .gitignore

# Ajouter tous les fichiers
git add .
git commit -m "Initial commit - Maalem Platform"

# Créer un repo sur GitHub et pousser
# Allez sur github.com, créez un nouveau repo "maalem-platform"
# Puis exécutez:
git remote add origin https://github.com/VOTRE_USERNAME/maalem-platform.git
git branch -M main
git push -u origin main
```

### Étape 2: Déployer le Frontend sur Vercel

#### 2.1 Préparer les variables d'environnement

Créez `.env.production` dans le dossier frontend:

```env
VITE_API_URL=https://votre-backend.onrender.com/api
```

#### 2.2 Déployer sur Vercel

1. Allez sur [vercel.com](https://vercel.com)
2. Connectez-vous avec GitHub
3. Cliquez sur "Import Project"
4. Sélectionnez votre repo GitHub
5. Configurez:
   - **Framework Preset**: Vite
   - **Root Directory**: `maalem-frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

6. Ajoutez les variables d'environnement:
   - `VITE_API_URL` = `https://votre-backend.onrender.com/api`

7. Cliquez sur "Deploy"

### Étape 3: Déployer le Backend sur Render

#### 3.1 Créer les fichiers nécessaires

Créez `requirements.txt` dans `maalem-backend`:

```txt
Django==5.0.0
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1
django-cors-headers==4.3.1
django-filter==23.5
Pillow==10.1.0
psycopg2-binary==2.9.9
channels==4.0.0
channels-redis==4.1.0
redis==5.0.1
daphne==4.0.0
gunicorn==21.2.0
whitenoise==6.6.0
python-dotenv==1.0.0
```

Créez `build.sh` dans `maalem-backend`:

```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
```

Créez `render.yaml` à la racine du projet:

```yaml
services:
  - type: web
    name: maalem-backend
    env: python
    region: frankfurt
    plan: free
    buildCommand: "./build.sh"
    startCommand: "gunicorn config.wsgi:application"
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: maalem-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: DJANGO_SETTINGS_MODULE
        value: config.settings
      - key: DEBUG
        value: False
      - key: ALLOWED_HOSTS
        value: .onrender.com
      - key: CORS_ALLOWED_ORIGINS
        value: https://votre-frontend.vercel.app

databases:
  - name: maalem-db
    region: frankfurt
    plan: free
```

#### 3.2 Déployer sur Render

1. Allez sur [render.com](https://render.com)
2. Connectez-vous avec GitHub
3. Cliquez sur "New +" → "Web Service"
4. Sélectionnez votre repo
5. Configurez:
   - **Name**: maalem-backend
   - **Region**: Frankfurt
   - **Branch**: main
   - **Root Directory**: `maalem-backend`
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application`

6. Ajoutez les variables d'environnement (comme dans render.yaml)
7. Créez une base de données PostgreSQL (gratuite)
8. Cliquez sur "Create Web Service"

### Étape 4: Configurer CORS et URLs

Une fois déployé, mettez à jour:

1. **Backend** - Ajoutez l'URL Vercel à `CORS_ALLOWED_ORIGINS`
2. **Frontend** - Mettez à jour `VITE_API_URL` avec l'URL Render
3. Redéployez les deux services

---

## Option 2: Réseau Local 🏠

Pour accéder au site depuis d'autres appareils sur votre réseau local.

### Étape 1: Trouver votre IP locale

```powershell
ipconfig
# Cherchez "Adresse IPv4" (ex: 192.168.1.100)
```

### Étape 2: Configurer le Backend

Modifiez `maalem-backend/.env`:

```env
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,192.168.1.100
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://192.168.1.100:5173
```

### Étape 3: Démarrer les serveurs

```powershell
# Backend
cd "c:\Users\Igolan\Desktop\site maalem\maalem-backend"
python manage.py runserver 0.0.0.0:8000

# Frontend (dans un nouveau terminal)
cd "c:\Users\Igolan\Desktop\site maalem\maalem-frontend"
npm run dev -- --host 0.0.0.0
```

### Étape 4: Accéder au site

Sur n'importe quel appareil du même réseau:
- Ouvrez `http://192.168.1.100:5173`

---

## Option 3: Tunnel ngrok (Temporaire) 🌐

Pour un accès public temporaire (gratuit).

### Étape 1: Installer ngrok

1. Téléchargez [ngrok](https://ngrok.com/download)
2. Créez un compte gratuit
3. Authentifiez-vous: `ngrok authtoken VOTRE_TOKEN`

### Étape 2: Créer des tunnels

```powershell
# Terminal 1 - Backend
cd "c:\Users\Igolan\Desktop\site maalem\maalem-backend"
python manage.py runserver

# Terminal 2 - Tunnel Backend
ngrok http 8000

# Terminal 3 - Frontend (mettez à jour VITE_API_URL avec l'URL ngrok)
cd "c:\Users\Igolan\Desktop\site maalem\maalem-frontend"
npm run dev

# Terminal 4 - Tunnel Frontend
ngrok http 5173
```

### Étape 3: Configurer CORS

Ajoutez les URLs ngrok à votre backend `.env`:

```env
CORS_ALLOWED_ORIGINS=https://votre-url.ngrok-free.app
ALLOWED_HOSTS=votre-url.ngrok-free.app
```

⚠️ **Note**: Les URLs ngrok changent à chaque redémarrage (version gratuite).

---

## 📝 Checklist Finale

Avant de rendre public:

- [ ] ✅ Changez `DEBUG=False` en production
- [ ] ✅ Utilisez une SECRET_KEY sécurisée
- [ ] ✅ Configurez une base de données PostgreSQL
- [ ] ✅ Configurez les médias (AWS S3 ou similaire)
- [ ] ✅ Activez HTTPS (automatique avec Vercel/Render)
- [ ] ✅ Testez toutes les fonctionnalités
- [ ] ✅ Sauvegardez votre base de données

---

## 🆘 Support

Si vous rencontrez des problèmes:

1. Vérifiez les logs sur Vercel/Render
2. Vérifiez CORS et ALLOWED_HOSTS
3. Testez l'API avec Postman
4. Consultez la documentation Django/Vite

---

## 🎉 Félicitations!

Votre site est maintenant accessible publiquement! 🚀

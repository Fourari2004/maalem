# 🚀 Démarrage Rapide - Accès Public

## Option 1: Accès Réseau Local (Immédiat) 📱

Pour rendre le site accessible sur votre réseau WiFi local:

### Méthode Automatique ⚡

1. **Double-cliquez** sur `start_public.ps1`
2. Si Windows bloque, clic droit → "Exécuter avec PowerShell"
3. Suivez les instructions à l'écran
4. Votre site sera accessible à `http://VOTRE_IP:5173`

### Méthode Manuelle 🔧

```powershell
# 1. Trouver votre IP
ipconfig
# Cherchez "Adresse IPv4" (ex: 192.168.1.100)

# 2. Démarrer le backend
cd "c:\Users\Igolan\Desktop\site maalem\maalem-backend"
python manage.py runserver 0.0.0.0:8000

# 3. Dans un nouveau terminal, démarrer le frontend
cd "c:\Users\Igolan\Desktop\site maalem\maalem-frontend"
npm run dev -- --host 0.0.0.0

# 4. Accéder depuis n'importe quel appareil
# http://192.168.1.100:5173 (remplacez par votre IP)
```

---

## Option 2: Déploiement Internet (Permanent) 🌐

Pour un accès depuis n'importe où sur Internet.

### A. Frontend sur Vercel (Gratuit)

1. **Créer un compte** sur [vercel.com](https://vercel.com)
2. **Installer Vercel CLI**:
   ```powershell
   npm install -g vercel
   ```

3. **Déployer**:
   ```powershell
   cd "c:\Users\Igolan\Desktop\site maalem\maalem-frontend"
   vercel
   ```

4. **Suivez les instructions**:
   - Login avec GitHub
   - Confirmez le projet
   - Attendez le déploiement
   - Notez l'URL: `https://votre-projet.vercel.app`

### B. Backend sur Render (Gratuit)

1. **Créer un compte** sur [render.com](https://render.com)

2. **Pusher le code sur GitHub**:
   ```powershell
   cd "c:\Users\Igolan\Desktop\site maalem"
   git init
   git add .
   git commit -m "Initial commit"
   
   # Créez un repo sur GitHub, puis:
   git remote add origin https://github.com/VOTRE_USERNAME/maalem.git
   git push -u origin main
   ```

3. **Sur Render**:
   - New → Web Service
   - Connectez votre repo GitHub
   - Root Directory: `maalem-backend`
   - Build Command: `./build.sh`
   - Start Command: `gunicorn config.wsgi:application`
   - Créez une base PostgreSQL
   - Ajoutez les variables d'environnement
   - Deploy!

4. **Mettre à jour les URLs**:
   - Frontend `.env.production`: `VITE_API_URL=https://votre-backend.onrender.com/api`
   - Backend: Ajoutez l'URL Vercel à `CORS_ALLOWED_ORIGINS`

---

## Option 3: Tunnel ngrok (Temporaire) ⏰

Pour un accès Internet temporaire (idéal pour les tests):

1. **Télécharger** [ngrok](https://ngrok.com/download)

2. **S'inscrire** sur ngrok.com

3. **Authentifier**:
   ```powershell
   ngrok authtoken VOTRE_TOKEN
   ```

4. **Démarrer les serveurs normalement**:
   ```powershell
   # Terminal 1
   cd maalem-backend
   python manage.py runserver
   
   # Terminal 2
   cd maalem-frontend
   npm run dev
   ```

5. **Créer des tunnels**:
   ```powershell
   # Terminal 3
   ngrok http 8000
   # Note l'URL: https://xxxx.ngrok-free.app
   
   # Terminal 4
   ngrok http 5173
   # Note l'URL: https://yyyy.ngrok-free.app
   ```

6. **Mettre à jour les configurations**:
   - Frontend: `VITE_API_URL=https://xxxx.ngrok-free.app/api`
   - Backend `.env`: `CORS_ALLOWED_ORIGINS=https://yyyy.ngrok-free.app`
   - Backend `.env`: `ALLOWED_HOSTS=xxxx.ngrok-free.app`

⚠️ **Note**: Les URLs changent à chaque redémarrage (version gratuite)

---

## 🔒 Configuration Pare-feu Windows

Si le site n'est pas accessible depuis d'autres appareils:

1. **Ouvrir** Pare-feu Windows
2. **Paramètres avancés**
3. **Règles de trafic entrant** → Nouvelle règle
4. **Port** → TCP → Ports spécifiques: `8000, 5173`
5. **Autoriser la connexion**
6. **Appliquer à**: Privé, Public
7. **Nom**: "Maalem Site"

---

## 📊 Comparaison des Options

| Option | Gratuit | Permanent | Internet | Difficulté | Temps |
|--------|---------|-----------|----------|------------|-------|
| Réseau Local | ✅ | ✅ | ❌ | Facile | 2 min |
| Vercel + Render | ✅ | ✅ | ✅ | Moyen | 30 min |
| ngrok | ✅ | ❌ | ✅ | Facile | 5 min |

---

## 🆘 Problèmes Courants

### Le site ne charge pas
- Vérifiez que les deux serveurs sont démarrés
- Vérifiez le pare-feu
- Vérifiez l'IP dans les configurations

### Erreur CORS
- Vérifiez `CORS_ALLOWED_ORIGINS` dans le backend
- Redémarrez le serveur backend après modification

### 502 Bad Gateway
- Le backend n'est pas démarré ou accessible
- Vérifiez l'URL de l'API dans le frontend

---

## ✅ Checklist

Avant de rendre public:

- [ ] Les serveurs démarrent sans erreur
- [ ] L'API répond correctement
- [ ] CORS est configuré
- [ ] Base de données est migrée
- [ ] Variables d'environnement configurées
- [ ] Pare-feu autorise les connexions
- [ ] Testé depuis un autre appareil

---

## 🎉 C'est Prêt!

Votre site Maalem est maintenant accessible publiquement! 🚀

**Besoin d'aide?** Consultez le [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) complet.

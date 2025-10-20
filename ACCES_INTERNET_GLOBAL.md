# ACCÈS DEPUIS N'IMPORTE QUEL WIFI - Configuration avec ngrok

## 🌍 Vue d'ensemble

Cette configuration permet à n'importe qui, sur n'importe quel réseau WiFi/Internet, d'accéder à votre site.

## 📋 Prérequis

### 1. Installer ngrok

1. Allez sur: https://ngrok.com/download
2. Téléchargez ngrok pour Windows
3. Créez un compte gratuit sur: https://dashboard.ngrok.com/signup
4. Extrayez `ngrok.exe` dans un dossier (par exemple: `C:\ngrok\`)

### 2. Configurer ngrok

1. Allez sur: https://dashboard.ngrok.com/get-started/your-authtoken
2. Copiez votre authtoken
3. Ouvrez PowerShell et exécutez:
   ```powershell
   C:\ngrok\ngrok.exe config add-authtoken VOTRE_TOKEN_ICI
   ```

## 🚀 Lancement

### Terminal 1 - Backend Django
```bash
cd maalem-backend
python manage.py runserver 0.0.0.0:8000
```

### Terminal 2 - Frontend Vite
```bash
cd maalem-frontend
npm run dev -- --host
```

### Terminal 3 - Tunnel ngrok pour le Backend
```bash
C:\ngrok\ngrok.exe http 8000
```

### Terminal 4 - Tunnel ngrok pour le Frontend
```bash
C:\ngrok\ngrok.exe http 5173
```

## 📝 Configuration après le lancement

Après avoir lancé ngrok, vous verrez quelque chose comme:
```
Forwarding   https://abcd-1234-5678.ngrok-free.app -> http://localhost:8000
```

### Étape 1: Noter les URLs ngrok
- URL Backend: `https://xxxx-backend.ngrok-free.app`
- URL Frontend: `https://yyyy-frontend.ngrok-free.app`

### Étape 2: Mettre à jour la configuration

1. **Mettre à jour le backend** - Fichier: `maalem-backend\config\settings.py`
   ```python
   ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.68.58', 'xxxx-backend.ngrok-free.app']
   
   CORS_ALLOWED_ORIGINS = [
       'http://localhost:5173',
       'https://yyyy-frontend.ngrok-free.app',  # Ajoutez votre URL ngrok frontend
   ]
   ```

2. **Créer `.env.ngrok`** dans `maalem-frontend`:
   ```
   VITE_API_URL=https://xxxx-backend.ngrok-free.app/api
   ```

3. **Appliquer la configuration**:
   ```bash
   cd maalem-frontend
   copy .env.ngrok .env
   ```

4. **Redémarrer le frontend**

### Étape 3: Partager le lien
Partagez l'URL frontend ngrok: `https://yyyy-frontend.ngrok-free.app`

N'importe qui avec ce lien peut maintenant accéder au site depuis n'importe quel réseau WiFi/4G/5G dans le monde!

## ⚡ Script Automatique

Je vais créer un script qui lance tout automatiquement.

## ⚠️ Limitations Version Gratuite ngrok

- Les URLs changent à chaque redémarrage
- Session limitée à 8 heures
- Bannière ngrok affichée sur le site
- 40 connexions/minute maximum

## 💎 Version Payante ngrok (Recommandé pour usage régulier)

- URLs personnalisées fixes (ex: `maalem.ngrok.app`)
- Pas de limite de temps
- Pas de bannière
- Plus de connexions simultanées
- Prix: ~$8/mois

## 🌐 Alternative: Déploiement Cloud Permanent

Pour un accès permanent et professionnel, considérez le déploiement cloud:
- Frontend: Vercel (gratuit)
- Backend: Render / Railway (gratuit ou ~$5/mois)
- Voir: `DEPLOYMENT_GUIDE.md`

## 🔒 Sécurité

**IMPORTANT:** 
- Changez tous les mots de passe par défaut
- Utilisez des mots de passe forts
- Activez HTTPS (ngrok le fait automatiquement)
- Ne partagez pas les URLs ngrok publiquement si le site contient des données sensibles

## 📞 Support

Si vous avez des questions, consultez:
- Documentation ngrok: https://ngrok.com/docs
- Dashboard ngrok: https://dashboard.ngrok.com/

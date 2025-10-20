# 🌐 Comment Rendre le Site Maalem Public

## 🎯 Méthode Rapide (Recommandée)

### Pour Réseau Local WiFi 📱

**En 2 minutes, rendez votre site accessible depuis tous les appareils de votre maison/bureau:**

#### Étape 1: Configurer le Pare-feu (Une seule fois)

1. **Clic droit** sur `configure_firewall.ps1`
2. Sélectionnez **"Exécuter en tant qu'administrateur"**
3. Cliquez **"Oui"** pour autoriser les modifications
4. Attendez le message de succès

#### Étape 2: Démarrer le Site en Mode Public

1. **Double-cliquez** sur `start_public.ps1`
2. Si bloqué, **clic droit → "Exécuter avec PowerShell"**
3. Notez l'adresse IP affichée (ex: `192.168.1.100`)

#### Étape 3: Accéder au Site

**Depuis n'importe quel appareil sur le même WiFi:**
- Téléphone, tablette, ordinateur
- Ouvrez un navigateur
- Tapez: `http://192.168.1.100:5173` (utilisez votre IP)

---

## 🌍 Pour Internet Mondial

### Option A: Déploiement Gratuit (Permanent)

**Hébergement gratuit sur Vercel + Render:**

📖 Consultez le guide détaillé: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

**Résumé rapide:**
1. Créez des comptes sur [Vercel](https://vercel.com) et [Render](https://render.com)
2. Poussez votre code sur GitHub
3. Connectez les plateformes à votre repo
4. Configurez les variables d'environnement
5. Deploy!

⏱️ **Temps estimé**: 30-45 minutes
💰 **Coût**: Gratuit
✅ **Avantages**: Permanent, HTTPS, CDN, Domaine personnalisé

### Option B: Tunnel ngrok (Temporaire)

**Pour des tests rapides ou démos:**

📖 Guide détaillé: [QUICK_START_PUBLIC.md](QUICK_START_PUBLIC.md)

```powershell
# 1. Télécharger ngrok
https://ngrok.com/download

# 2. Démarrer les serveurs
cd maalem-backend
python manage.py runserver

cd maalem-frontend  # Nouveau terminal
npm run dev

# 3. Créer les tunnels
ngrok http 8000  # Nouveau terminal - Backend
ngrok http 5173  # Nouveau terminal - Frontend
```

⏱️ **Temps estimé**: 5 minutes
💰 **Coût**: Gratuit
⚠️ **Limitation**: URL change à chaque redémarrage

---

## 📋 Comparaison des Méthodes

| Méthode | Internet | Gratuit | Permanent | Difficulté | Temps |
|---------|----------|---------|-----------|------------|-------|
| **Réseau Local** | ❌ WiFi uniquement | ✅ | ✅ | 😊 Facile | 2 min |
| **Vercel + Render** | ✅ Mondial | ✅ | ✅ | 😐 Moyen | 30 min |
| **ngrok** | ✅ Mondial | ✅ | ❌ Temporaire | 😊 Facile | 5 min |

---

## 🔧 Fichiers Créés

Voici les fichiers que j'ai créés pour vous:

### Scripts
- `start_public.ps1` - Démarre le site en mode public (réseau local)
- `configure_firewall.ps1` - Configure le pare-feu Windows
- `build.sh` - Script de build pour Render

### Configuration
- `render.yaml` - Configuration pour déploiement Render
- `.env.production` - Variables d'environnement pour production
- `requirements.txt` - Dépendances Python
- `vercel.json` - Configuration Vercel (déjà existant)

### Documentation
- `DEPLOYMENT_GUIDE.md` - Guide complet de déploiement
- `QUICK_START_PUBLIC.md` - Guide de démarrage rapide
- `LANCER_SITE_PUBLIC.md` - Ce fichier

---

## ✅ Checklist Pré-Lancement

Avant de rendre public, vérifiez:

### Sécurité
- [ ] Changez `SECRET_KEY` en production
- [ ] Utilisez `DEBUG=False` en production
- [ ] Configurez HTTPS (automatique avec Vercel/Render)
- [ ] Changez les mots de passe par défaut

### Configuration
- [ ] Base de données configurée
- [ ] Variables d'environnement définies
- [ ] CORS configuré correctement
- [ ] Médias configurés (local ou S3)

### Tests
- [ ] Inscription client fonctionne
- [ ] Inscription artisan fonctionne
- [ ] Connexion fonctionne
- [ ] Création de posts fonctionne
- [ ] Notifications fonctionnent
- [ ] Messagerie fonctionne

---

## 🆘 Problèmes Courants

### "Le site ne charge pas"
✅ **Solutions:**
1. Vérifiez que les deux serveurs sont démarrés
2. Vérifiez votre pare-feu Windows
3. Vérifiez que vous êtes sur le même WiFi

### "CORS Error"
✅ **Solutions:**
1. Vérifiez `CORS_ALLOWED_ORIGINS` dans `.env`
2. Incluez votre IP ou domaine
3. Redémarrez le serveur backend

### "502 Bad Gateway"
✅ **Solutions:**
1. Le backend n'est pas démarré
2. Mauvaise URL d'API dans le frontend
3. Vérifiez les logs du backend

### "Cannot connect to database"
✅ **Solutions:**
1. PostgreSQL est-il démarré?
2. Vérifiez les credentials dans `.env`
3. Exécutez `python manage.py migrate`

---

## 📞 Besoin d'Aide?

### Documentation
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Guide complet
- [QUICK_START_PUBLIC.md](QUICK_START_PUBLIC.md) - Démarrage rapide
- [README.md](README.md) - Documentation générale

### Logs
```powershell
# Backend
cd maalem-backend
python manage.py runserver --verbosity 2

# Frontend
cd maalem-frontend
npm run dev -- --debug
```

### Vérification Réseau
```powershell
# Vérifier votre IP
ipconfig

# Tester la connexion backend
curl http://localhost:8000/api/

# Vérifier les ports ouverts
netstat -ano | findstr "8000"
netstat -ano | findstr "5173"
```

---

## 🎉 C'est Parti!

Vous êtes maintenant prêt à rendre votre site Maalem accessible au monde!

### Prochaines Étapes Recommandées

1. **Maintenant**: Démarrez en réseau local pour tester
2. **Cette semaine**: Déployez sur Vercel + Render pour un accès permanent
3. **Bientôt**: Configurez un nom de domaine personnalisé

**Félicitations pour avoir créé une plateforme complète! 🚀**

---

*Dernière mise à jour: 2025-10-19*

# Maalem - Plateforme des Artisans Marocains

![Maalem Platform](maalem-frontend/public/logo.png)

Maalem est une plateforme sociale dédiée aux artisans marocains, permettant aux utilisateurs de découvrir, suivre et interagir avec les meilleurs artisans du Maroc.

## Structure du Projet

```
.
├── maalem-backend/          # Django REST API Backend
│   ├── config/             # Configuration files
│   ├── maalem/             # Main application modules
│   │   ├── users/          # User management
│   │   ├── posts/          # Social posts
│   │   ├── chat/           # Real-time messaging
│   │   ├── notifications/  # Notification system
│   │   └── ...             # Other modules
│   ├── manage.py           # Django management script
│   └── requirements.txt    # Python dependencies
└── maalem-frontend/         # React/Vite Frontend
    ├── src/                # Source code
    ├── public/             # Static assets
    └── package.json        # Node.js dependencies
```

## Fonctionnalités

### Frontend (React/Vite)
- Interface responsive pour mobile et desktop
- Fil d'actualité des artisans
- Profils détaillés des artisans
- Messagerie en temps réel
- Création et partage de posts
- Système de notifications

### Backend (Django)
- API REST complète
- Authentification JWT
- Gestion des utilisateurs
- Système de messagerie en temps réel (WebSockets)
- Notifications push
- Gestion des médias (images, documents)

## Technologies Utilisées

### Backend
- Python 3.8+
- Django 4.x
- Django REST Framework
- PostgreSQL
- Redis (pour WebSockets)
- Django Channels (messagerie en temps réel)

### Frontend
- React 18
- Vite
- Tailwind CSS
- React Router v6
- Shadcn/ui Components

## Installation Locale

### Prérequis
- Python 3.8+
- Node.js 16+
- PostgreSQL
- Redis

### Backend
```bash
cd maalem-backend
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd maalem-frontend
npm install
npm run dev
```

### Démarrage rapide

Pour démarrer les deux serveurs simultanément, vous avez plusieurs options :

1. **Lancement en un clic (recommandé)** :
   ```powershell
   .\LANCER_TOUT.ps1
   ```
   OU
   ```cmd
   LANCER_TOUT.bat
   ```

2. **Script Windows PowerShell** :
   ```powershell
   .\start_servers.ps1
   ```

3. **Script Windows Batch** :
   ```cmd
   start_servers.bat
   ```

4. **Commandes manuelles** :
   ```bash
   # Terminal 1 - Backend
   cd maalem-backend
   python manage.py runserver
   
   # Terminal 2 - Frontend
   cd maalem-frontend
   npm run dev
   ```

Cela lancera à la fois le backend Django sur `http://localhost:8000` et le frontend React sur `http://localhost:5173`.

## Accès Réseau

L'application peut être accédée depuis différentes adresses IP:

### Frontend
- http://localhost:5173
- http://127.0.0.1:5173
- http://192.168.137.251:5173

### Backend API
- http://localhost:8000/api/
- http://127.0.0.1:8000/api/
- http://192.168.137.251:8000/api/

Pour configurer l'accès depuis d'autres adresses IP, consultez: [NETWORK_ACCESS_CONFIGURATION.md](NETWORK_ACCESS_CONFIGURATION.md)

## Résolution des Problèmes

### Problèmes de Connexion API
Si vous rencontrez des erreurs de connexion (`ERR_CONNECTION_TIMED_OUT`, `TypeError: Failed to fetch`) :

1. **Vérifiez que les deux serveurs sont en cours d'exécution**
2. **Vérifiez la configuration dans `maalem-frontend/.env`** :
   ```
   VITE_API_URL=http://localhost:8000/api
   ```
3. **Consultez le guide détaillé** : [CONNECTION_FIX_SUMMARY.md](CONNECTION_FIX_SUMMARY.md)

### Solution de Lancement en Un Clic
Tous les problèmes peuvent être résolus automatiquement en utilisant le script de lancement en un clic :
- [Documentation de la Solution](ONE_CLICK_LAUNCH_SOLUTION.md)
- [Script PowerShell](LANCER_TOUT.ps1)
- [Script Batch](LANCER_TOUT.bat)

### Documentation de Support
- [Guide de Démarrage](STARTUP_GUIDE.md) - Instructions détaillées pour démarrer l'application
- [Résumé des Corrections](FIX_SUMMARY.md) - Résumé des problèmes résolus et solutions appliquées
- [Documentation de la Correction API](API_CONNECTION_FIX.md) - Détails techniques sur la résolution du problème de connexion
- [Résumé de la Correction des Connexions](CONNECTION_FIX_SUMMARY.md) - Détails sur la correction des problèmes de connexion actuels
- [Configuration d'Accès Réseau](NETWORK_ACCESS_CONFIGURATION.md) - Configuration pour accéder depuis différentes adresses IP
- [Solution de Lancement en Un Clic](ONE_CLICK_LAUNCH_SOLUTION.md) - Documentation complète de la solution automatisée

## Déploiement

Pour déployer l'application en production, consultez le guide complet : [DEPLOYMENT.md](DEPLOYMENT.md)

### Options de déploiement recommandées :
- **Frontend** : Vercel
- **Backend** : Heroku
- **Base de données** : Heroku Postgres
- **Stockage des médias** : AWS S3 ou Cloudinary

## Documentation

- [Frontend README](maalem-frontend/README.md) - Documentation détaillée du frontend
- [Backend README](maalem-backend/README.md) - Documentation détaillée du backend
- [Guide de déploiement](DEPLOYMENT.md) - Instructions complètes pour déployer en production
- [Déploiement Frontend (Vercel)](maalem-frontend/DEPLOYMENT_VERCEL.md)
- [Déploiement Backend (Heroku)](maalem-backend/DEPLOYMENT_HEROKU.md)

## Contribution

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commitez vos modifications (`git commit -m 'Add some AmazingFeature'`)
4. Poussez la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## License

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus d'informations.

## Contact

Pour toute question ou suggestion, veuillez contacter l'équipe de développement.
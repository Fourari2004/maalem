# Maalem Backend - API Django

API backend pour la plateforme Maalem, construite avec Django et Django REST Framework.

## Structure du Projet

```
maalem-backend/
├── config/                 # Configuration Django
│   ├── settings.py         # Paramètres de l'application
│   ├── urls.py             # URLs principales
│   └── ...
├── maalem/                 # Applications Django
│   ├── users/              # Gestion des utilisateurs
│   ├── posts/              # Posts sociaux
│   ├── chat/               # Messagerie en temps réel
│   ├── notifications/      # Notifications
│   └── ...                 # Autres modules
├── manage.py               # Script de gestion Django
└── requirements.txt        # Dépendances Python
```

## Technologies Utilisées

- Python 3.8+
- Django 4.x
- Django REST Framework
- PostgreSQL
- Redis (pour WebSockets)
- Django Channels (messagerie en temps réel)
- JWT pour l'authentification

## Installation

1. Naviguez vers le dossier du backend :
   ```bash
   cd maalem-backend
   ```

2. Créez un environnement virtuel :
   ```bash
   python -m venv venv
   ```

3. Activez l'environnement virtuel :
   - Sur Windows :
     ```bash
     venv\Scripts\activate
     ```
   - Sur macOS/Linux :
     ```bash
     source venv/bin/activate
     ```

4. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

5. Créez un fichier `.env` à la racine du backend avec les variables d'environnement requises (voir [.env.example](file:///c%3A/Users/Igolan/Desktop/site%20maalem/maalem-backend/.env.example))

6. Lancez les migrations :
   ```bash
   python manage.py migrate
   ```

7. Démarrez le serveur de développement :
   ```bash
   python manage.py runserver
   ```

## Variables d'Environnement

Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=.localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Database
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password

# AWS S3 (for media storage)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=your-region
```

## API Endpoints

### Authentification
- `POST /api/auth/login/` - Connexion
- `POST /api/auth/register/` - Inscription
- `POST /api/auth/logout/` - Déconnexion

### Utilisateurs
- `GET /api/users/` - Liste des utilisateurs
- `GET /api/users/{id}/` - Détails d'un utilisateur
- `PUT /api/users/{id}/` - Mise à jour d'un utilisateur

### Posts
- `GET /api/posts/` - Liste des posts
- `POST /api/posts/` - Création d'un post
- `GET /api/posts/{id}/` - Détails d'un post
- `PUT /api/posts/{id}/` - Mise à jour d'un post
- `DELETE /api/posts/{id}/` - Suppression d'un post

### Messagerie
- `GET /api/chat/rooms/` - Liste des salons de discussion
- `GET /api/chat/rooms/{id}/messages/` - Messages d'un salon
- `POST /api/chat/rooms/{id}/messages/` - Envoi d'un message

### Notifications
- `GET /api/notifications/` - Liste des notifications
- `PUT /api/notifications/{id}/read/` - Marquer une notification comme lue

## Déploiement

Pour déployer le backend en production, consultez le guide : [DEPLOYMENT_HEROKU.md](DEPLOYMENT_HEROKU.md)

## Développement

### Création d'une nouvelle application

```bash
python manage.py startapp nom_de_l_application
```

N'oubliez pas d'ajouter la nouvelle application à `INSTALLED_APPS` dans [settings.py](file:///c%3A/Users/Igolan/Desktop/site%20maalem/maalem-backend/config/settings.py).

### Création de migrations

```bash
python manage.py makemigrations
```

### Application des migrations

```bash
python manage.py migrate
```

### Création d'un superutilisateur

```bash
python manage.py createsuperuser
```

## Tests

Pour exécuter les tests :

```bash
python manage.py test
```

## Contribution

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commitez vos modifications (`git commit -m 'Add some AmazingFeature'`)
4. Poussez la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## License

Ce projet est sous licence MIT - voir le fichier [LICENSE](../LICENSE) pour plus d'informations.
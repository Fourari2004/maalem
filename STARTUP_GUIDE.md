# Guide de Démarrage - Maalem Platform

## Problème Résolu
Erreur de connexion API : `ERR_CONNECTION_TIMED_OUT` et `TypeError: Failed to fetch`

## Solution Appliquée
1. Correction de la configuration réseau
2. Mise à jour des scripts de démarrage
3. Vérification des URLs d'API

## Instructions de Démarrage

### Méthode 1: PowerShell (Recommandée)
```powershell
# Depuis le répertoire racine du projet
.\start_servers.ps1
```

### Méthode 2: Lancement Manuel
1. **Démarrer le Backend (Django)**
   ```powershell
   cd "c:\Users\Igolan\Desktop\site maalem\maalem-backend"
   python manage.py runserver
   ```

2. **Démarrer le Frontend (React)**
   ```powershell
   cd "c:\Users\Igolan\Desktop\site maalem\maalem-frontend"
   npm run dev
   ```

### Méthode 3: Batch File
```cmd
start_servers.bat
```

## URLs d'Accès

- **Application Frontend**: http://localhost:5173
- **API Backend**: http://localhost:8000/api/
- **Documentation API**: http://localhost:8000/api/docs/

## Vérification de la Connexion

### Test Backend
```bash
curl http://localhost:8000/api/posts/
```

### Test Frontend
Ouvrez http://localhost:5173 dans votre navigateur

## Résolution des Problèmes

### 1. Erreur de Connexion API
**Symptômes**: 
- `ERR_CONNECTION_TIMED_OUT`
- `TypeError: Failed to fetch`

**Solutions**:
- Vérifiez que le backend est en cours d'exécution
- Vérifiez le fichier `.env` dans `maalem-frontend`
- Assurez-vous que les URLs correspondent: `http://localhost:8000/api`

### 2. Problèmes de Configuration
**Vérifiez le fichier**: `maalem-frontend/.env`
**Contenu correct**:
```
VITE_API_URL=http://localhost:8000/api
```

### 3. Problèmes de Chemin
Si vous obtenez des erreurs de chemin:
- Utilisez des chemins absolus avec guillemets
- Vérifiez que vous êtes dans le bon répertoire

## Ports Utilisés

- **Frontend**: 5173 (Vite)
- **Backend**: 8000 (Django)
- **Redis**: 6379 (si utilisé pour WebSockets)
- **PostgreSQL**: 5432 (si utilisé localement)

## Commandes Utiles

### Redémarrer les Serveurs
```powershell
# Tuer les processus existants
taskkill /f /im python.exe
taskkill /f /im node.exe

# Redémarrer
.\start_servers.ps1
```

### Vérifier les Ports
```powershell
# Vérifier si le port 8000 est utilisé
netstat -ano | findstr :8000

# Vérifier si le port 5173 est utilisé
netstat -ano | findstr :5173
```

## Configuration Environnement

### Variables d'Environnement Requises

**Frontend** (`maalem-frontend/.env`):
```
VITE_API_URL=http://localhost:8000/api
```

**Backend** (`maalem-backend/.env`):
```
DEBUG=True
SECRET_KEY=votre_secret_key_ici
DATABASE_URL=postgresql://utilisateur:motdepasse@localhost:5432/nom_base
```

## Dépannage Avancé

### Logs du Backend
Les logs du serveur Django s'affichent dans le terminal où vous avez exécuté `python manage.py runserver`

### Logs du Frontend
Les logs du serveur Vite s'affichent dans le terminal où vous avez exécuté `npm run dev`

### Erreurs Courantes

1. **EADDRINUSE**: Un autre service utilise le port
   - Solution: Changez le port ou arrêtez le service conflictuel

2. **EACCES**: Problème de permissions
   - Solution: Exécutez en tant qu'administrateur ou changez de port

3. **ENOTFOUND**: Problème DNS
   - Solution: Utilisez `localhost` au lieu d'une IP spécifique

## Support

Si vous continuez à rencontrer des problèmes:
1. Vérifiez que tous les prérequis sont installés
2. Consultez le fichier [API_CONNECTION_FIX.md](API_CONNECTION_FIX.md)
3. Contactez l'équipe de développement
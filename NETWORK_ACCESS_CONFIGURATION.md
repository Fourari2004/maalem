# Configuration d'Accès Réseau pour Maalem

## Problème Résolu
Erreur lors du chargement des artisans: `Failed to fetch` depuis l'adresse IP `http://10.36.49.242:5173`

## Solution Appliquée
Configuration du backend pour accepter les requêtes CORS depuis l'adresse IP `10.36.49.242:5173`

## Configuration Actuelle

### Backend (.env)
```env
# Hosts autorisés
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,192.168.68.58,10.36.49.242

# Origines CORS autorisées
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://192.168.68.58:5173,http://10.36.49.242:5173
```

### Frontend (.env)
```env
# Configuration pour le développement local
VITE_API_URL=http://localhost:8000/api
```

## Adresses IP Prises en Charge

### Frontend
- `http://localhost:5173`
- `http://127.0.0.1:5173`
- `http://192.168.68.58:5173`
- `http://10.36.49.242:5173`

### Backend
- `http://localhost:8000`
- `http://127.0.0.1:8000`
- `http://192.168.68.58:8000`
- `http://10.36.49.242:8000`

## Test de Validation

### Résultats du Test
```
Testing from origin: http://10.36.49.242:5173
  OPTIONS request: 401
  CORS header: http://10.36.49.242:5173
  GET request: 200
  Posts count: 5
```

✅ Le frontend à l'adresse `http://10.36.49.242:5173` peut maintenant accéder à l'API backend.

## Instructions de Démarrage

### 1. Démarrer le Backend
```powershell
cd "c:\Users\Igolan\Desktop\site maalem\maalem-backend"
python manage.py runserver
```

### 2. Démarrer le Frontend
```powershell
cd "c:\Users\Igolan\Desktop\site maalem\maalem-frontend"
npm run dev
```

### 3. Accéder à l'Application
Vous pouvez maintenant accéder à l'application depuis:
- http://localhost:5173
- http://10.36.49.242:5173

## Résolution des Problèmes

### Si vous rencontrez encore des erreurs "Failed to fetch":

1. **Vérifiez que les serveurs sont en cours d'exécution**
   ```powershell
   # Vérifier les processus Python
   Get-Process python
   ```

2. **Vérifiez la configuration CORS**
   - Fichier: `maalem-backend/.env`
   - Vérifiez que votre IP est dans `ALLOWED_HOSTS` et `CORS_ALLOWED_ORIGINS`

3. **Redémarrez les serveurs**
   ```powershell
   # Tuer les processus existants
   Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
   Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
   
   # Redémarrer
   .\start_servers.ps1
   ```

### Erreurs Courantes

1. **ERR_CONNECTION_REFUSED**: Le serveur backend n'est pas démarré
2. **CORS error**: L'origine n'est pas autorisée dans la configuration CORS
3. **ERR_CONNECTION_TIMED_OUT**: Problème de pare-feu ou de réseau

## Configuration du Pare-feu (si nécessaire)

### Windows Defender Firewall
1. Ouvrez "Windows Defender Firewall avec sécurité avancée"
2. Cliquez sur "Règles de trafic entrant" → "Nouvelle règle"
3. Sélectionnez "Port" → Suivant
4. Sélectionnez "TCP" et spécifiez les ports "8000,5173" → Suivant
5. Sélectionnez "Autoriser la connexion" → Suivant
6. Cochez tous les profils → Suivant
7. Nommez la règle "Maalem Development" → Terminer

## Support

Pour toute question supplémentaire:
1. Vérifiez cette documentation
2. Exécutez le script de test: `python test_new_ip.py`
3. Contactez l'équipe de développement
# GUIDE D'ACCÈS MOBILE - Comment accéder au site depuis votre téléphone

## Problème
Quand vous essayez de vous connecter depuis votre téléphone, vous voyez:
> "Impossible de se connecter au serveur. Veuillez vérifier que le serveur backend est en cours d'exécution sur http://localhost:8000."

**Raison:** `localhost` ne fonctionne pas sur un téléphone car il fait référence au téléphone lui-même, pas à votre ordinateur.

## Solution Rapide

### Étape 1: Arrêter les serveurs actuels
Si les serveurs sont en cours d'exécution, arrêtez-les avec `Ctrl+C`

### Étape 2: Lancer le backend pour l'accès réseau
Ouvrez un terminal dans le dossier `maalem-backend`:
```bash
cd maalem-backend
python manage.py runserver 0.0.0.0:8000
```

**Important:** Utilisez `0.0.0.0:8000` au lieu de juste `8000` pour accepter les connexions depuis le réseau local.

### Étape 3: Lancer le frontend pour l'accès mobile

**Option A - Script automatique (Recommandé):**
Double-cliquez sur `start_mobile.bat` à la racine du projet.

**Option B - Ligne de commande:**
```bash
cd maalem-frontend
copy .env.mobile .env
npm run dev -- --host
```

### Étape 4: Accéder depuis votre téléphone
1. Assurez-vous que votre téléphone est sur le **MÊME réseau WiFi** que votre ordinateur
2. Sur votre téléphone, ouvrez le navigateur et allez à:
   ```
   http://192.168.68.58:5173
   ```

## Configuration du Pare-feu Windows

Si votre téléphone ne peut toujours pas se connecter, vous devez peut-être autoriser les ports dans le pare-feu:

### PowerShell (Exécuter en tant qu'administrateur):
```powershell
# Autoriser le port 8000 (Backend Django)
New-NetFirewallRule -DisplayName "Django Backend (Port 8000)" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow

# Autoriser le port 5173 (Frontend Vite)
New-NetFirewallRule -DisplayName "Vite Frontend (Port 5173)" -Direction Inbound -LocalPort 5173 -Protocol TCP -Action Allow
```

## Vérification

### Sur votre ordinateur:
- Backend: http://localhost:8000/api/
- Frontend: http://localhost:5173

### Depuis votre téléphone (même réseau WiFi):
- Frontend: http://192.168.68.58:5173

## Dépannage

### Le téléphone ne se connecte toujours pas?

1. **Vérifier l'IP de votre ordinateur:**
   ```bash
   ipconfig
   ```
   Cherchez "Adresse IPv4" sous "Carte réseau sans fil Wi-Fi"
   - Si elle a changé (différente de 192.168.68.58), mettez à jour:
     - `.env.mobile` avec la nouvelle IP
     - `start_mobile.bat` avec la nouvelle IP

2. **Vérifier le réseau WiFi:**
   - Ordinateur et téléphone doivent être sur le même réseau
   - Pas de VPN actif qui pourrait bloquer la connexion locale

3. **Tester la connexion:**
   Depuis votre téléphone, essayez d'abord:
   ```
   http://192.168.68.58:8000/api/
   ```
   Si cela ne fonctionne pas, c'est un problème de réseau/pare-feu.

4. **Pare-feu d'antivirus:**
   Certains antivirus (Norton, McAfee, Kaspersky) ont leur propre pare-feu.
   Ajoutez des exceptions pour les ports 5173 et 8000.

## Retour au mode localhost normal

Pour revenir à l'utilisation localhost normale:
```bash
cd maalem-frontend
copy .env.mobile .env  # Revient à la config localhost
# OU
del .env
# Le fichier .env sera recréé au prochain lancement
```

## Notes importantes

- **Sécurité:** Cette configuration est UNIQUEMENT pour le développement local
- **Production:** Ne jamais utiliser `0.0.0.0` ou des IPs locales en production
- **IP dynamique:** Votre adresse IP locale peut changer. Vérifiez-la avec `ipconfig` si la connexion échoue après un redémarrage

## Résumé des modifications effectuées

1. ✅ Mis à jour `ALLOWED_HOSTS` dans Django pour inclure `192.168.68.58`
2. ✅ Mis à jour `CORS_ALLOWED_ORIGINS` pour inclure `http://192.168.68.58:5173`
3. ✅ Créé `.env.mobile` avec l'API URL correcte
4. ✅ Créé `start_mobile.bat` pour un lancement facile
5. ✅ Créé `start_mobile.ps1` pour PowerShell

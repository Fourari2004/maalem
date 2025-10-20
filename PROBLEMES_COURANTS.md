# 🔧 Problèmes Courants et Solutions

## ❌ Erreur HTTP 400 - "Invalid HTTP_HOST header"

### Symptôme
```
Erreur lors du chargement des artisans: HTTP error! status: 400
```

Dans les logs Django:
```
Invalid HTTP_HOST header: '192.168.68.58:8000'. 
You may need to add '192.168.68.58' to ALLOWED_HOSTS.
```

### Cause
Django bloque les requêtes provenant d'hôtes non autorisés pour des raisons de sécurité. Quand vous accédez au site depuis votre téléphone via l'IP locale (192.168.68.58), Django doit avoir cette IP dans la liste ALLOWED_HOSTS.

### Solution

#### ✅ Solution Permanente (Déjà Appliquée)
Le fichier `maalem-backend/config/settings.py` a été mis à jour pour inclure votre IP:

```python
ALLOWED_HOSTS = [host.strip() for host in os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,192.168.68.58').split(',')]
```

#### 🔄 Si votre IP change
Si votre adresse IP locale change (après redémarrage du routeur):

1. **Trouvez votre nouvelle IP:**
   ```bash
   ipconfig
   ```
   Cherchez "Adresse IPv4" sous "Carte réseau sans fil Wi-Fi"

2. **Modifiez settings.py:**
   Remplacez `192.168.68.58` par votre nouvelle IP dans la ligne ALLOWED_HOSTS

3. **Redémarrez le backend:**
   Le serveur se recharge automatiquement, mais si ce n'est pas le cas:
   - Fermez la fenêtre du backend
   - Relancez `LANCER_TOUT.bat`

---

## ❌ Erreur: Le téléphone ne se connecte pas

### Symptômes
- Le téléphone affiche "Impossible de se connecter"
- Timeout ou "ERR_CONNECTION_REFUSED"

### Solutions

#### 1. Vérifier le même WiFi
✅ Ordinateur et téléphone DOIVENT être sur le même réseau WiFi

#### 2. Vérifier les serveurs
✅ Backend (port 8000) et Frontend (port 5173) doivent être lancés

Vérifiez dans les fenêtres de terminal que vous voyez:
```
Starting development server at http://0.0.0.0:8000/
```
et
```
➜  Network: http://192.168.68.58:5173/
```

#### 3. Configurer le pare-feu
✅ Lancez (en administrateur):
```bash
configure_firewall.ps1
```

Ou manuellement:
```powershell
New-NetFirewallRule -DisplayName "Django Backend" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "Vite Frontend" -Direction Inbound -LocalPort 5173 -Protocol TCP -Action Allow
```

#### 4. Vérifier l'URL
✅ Utilisez l'URL affichée dans LANCER_TOUT.bat, par exemple:
```
http://192.168.68.58:5173
```

Pas:
- ❌ `http://localhost:5173` (ne fonctionne pas sur le téléphone)
- ❌ `https://...` (pas de HTTPS en local)

---

## ❌ Erreur: "Python n'est pas reconnu"

### Symptôme
```
'python' n'est pas reconnu en tant que commande interne
```

### Solution
1. Installez Python: https://www.python.org/downloads/
2. Pendant l'installation: ✅ Cochez "Add Python to PATH"
3. Redémarrez l'ordinateur
4. Testez: `python --version`

---

## ❌ Erreur: "npm n'est pas reconnu"

### Symptôme
```
'npm' n'est pas reconnu en tant que commande interne
```

### Solution
1. Installez Node.js: https://nodejs.org/
2. Choisissez la version LTS (recommandée)
3. Redémarrez l'ordinateur
4. Testez: `npm --version`

---

## ❌ Erreur: Port déjà utilisé

### Symptôme
```
Error: That port is already in use.
```
ou
```
Address already in use
```

### Solution

#### Pour Windows:
```bash
# Trouver le processus qui utilise le port 8000
netstat -ano | findstr :8000

# Noter le PID (dernier nombre)
# Tuer le processus (remplacez PID par le numéro):
taskkill /PID <PID> /F
```

#### Ou simplement:
1. Fermez toutes les fenêtres de terminal
2. Redémarrez l'ordinateur
3. Relancez `LANCER_TOUT.bat`

---

## ❌ Erreur: CORS / Cross-Origin

### Symptôme
```
Access to fetch at 'http://192.168.68.58:8000/api/...' from origin 'http://192.168.68.58:5173' has been blocked by CORS policy
```

### Solution
Cette configuration est déjà faite dans `settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://192.168.68.58:5173',
    ...
]
```

Si le problème persiste après changement d'IP:
1. Ajoutez votre nouvelle IP dans `CORS_ALLOWED_ORIGINS`
2. Redémarrez le backend

---

## ❌ Erreur: Base de données

### Symptôme
```
django.db.utils.OperationalError: FATAL: password authentication failed
```

### Solution
Vérifiez le fichier `.env` dans `maalem-backend`:
```
DB_NAME=votre_base
DB_USER=votre_user
DB_PASSWORD=votre_password
DB_HOST=localhost
DB_PORT=5432
```

Assurez-vous que PostgreSQL est lancé.

---

## ❌ Erreur: Migrations non appliquées

### Symptôme
```
You have 18 unapplied migration(s)...
```

### Solution
```bash
cd maalem-backend
python manage.py migrate
```

---

## 🔍 Diagnostic Rapide

Lancez ce script pour vérifier votre installation:
```bash
TEST_LANCEMENT.bat
```

Il vérifie:
- ✅ Python installé
- ✅ Node.js installé
- ✅ npm installé
- ✅ Dossiers backend/frontend présents
- ✅ Détection IP

---

## 📞 Ordre de Dépannage

1. **Vérifiez les prérequis**
   ```bash
   TEST_LANCEMENT.bat
   ```

2. **Vérifiez que les serveurs sont lancés**
   - Fenêtre backend active
   - Fenêtre frontend active
   - Pas d'erreurs rouges dans les terminaux

3. **Vérifiez le réseau**
   - Même WiFi
   - IP correcte (utilisez `ipconfig`)
   - Pare-feu configuré

4. **Vérifiez les logs**
   - Regardez les fenêtres backend/frontend
   - Notez les erreurs exactes
   - Cherchez dans ce document

5. **En dernier recours**
   - Fermez tout
   - Redémarrez l'ordinateur
   - Relancez `LANCER_TOUT.bat`

---

## 💡 Prévention

### Checklist avant de lancer
- [ ] Python et Node.js installés
- [ ] PostgreSQL lancé
- [ ] Aucun autre serveur sur les ports 8000/5173
- [ ] Pare-feu configuré (première fois)
- [ ] WiFi activé

### Bonnes pratiques
- ✅ Utilisez toujours `LANCER_TOUT.bat` pour éviter les oublis
- ✅ Gardez les fenêtres de serveur ouvertes et visibles
- ✅ Ne fermez pas les terminaux pendant que vous développez
- ✅ Vérifiez l'IP si la connexion mobile ne fonctionne plus

---

## 📚 Ressources

- Guide complet: `LANCEMENT_1_CLIC.txt`
- Tous les guides: `INDEX_GUIDES.md`
- Comparaison options: `COMPARAISON_OPTIONS_ACCES.md`

---

**Dernière mise à jour:** 2025-10-19
**Version:** 1.0

# 🧪 Guide de Test - Notifications de Bienvenue

## ⚠️ Important - Redémarrage Nécessaire

Puisque nous avons modifié des fichiers backend et frontend, vous devez redémarrer les serveurs pour que les changements prennent effet.

---

## 🔄 Étape 1: Redémarrer les Serveurs

### Backend (Django)
1. Si le serveur backend est en cours d'exécution, arrêtez-le (Ctrl+C)
2. Redémarrez avec:
   ```powershell
   cd "C:\Users\Igolan\Desktop\site maalem\maalem-backend"
   python manage.py runserver 0.0.0.0:8000
   ```

### Frontend (React + Vite)
1. Si le serveur frontend est en cours d'exécution, arrêtez-le (Ctrl+C)
2. Redémarrez avec:
   ```powershell
   cd "C:\Users\Igolan\Desktop\site maalem\maalem-frontend"
   npm run dev
   ```

---

## 🧪 Étape 2: Test de la Notification de Bienvenue

### Test avec Nouvel Utilisateur

1. **Ouvrez votre navigateur** à http://192.168.68.58:5173 (ou localhost:5173)

2. **Ouvrez la Console du Navigateur**
   - Appuyez sur F12
   - Allez dans l'onglet "Network" (Réseau)
   - Gardez-le ouvert pour voir les requêtes

3. **Déconnectez-vous** (si vous êtes connecté)
   - Cliquez sur votre profil
   - Cliquez sur "Déconnexion"

4. **Inscrivez-vous avec un nouveau compte**
   - Cliquez sur "S'inscrire"
   - Remplissez le formulaire avec:
     - Email: **IMPORTANT: Utilisez un email UNIQUE** (ex: test123@example.com)
     - Prénom: Votre prénom
     - Nom: Votre nom
     - Ville: Choisissez une ville
     - Type: Artisan ou Client
     - Si Artisan: Choisissez une spécialité
     - Téléphone: Un numéro valide
     - Mot de passe: Créez un mot de passe
   
5. **Cliquez sur "S'inscrire"**
   - Attendez la confirmation
   - Vous devriez être connecté automatiquement

6. **Ouvrez le Panneau de Notifications**
   - Cliquez sur l'icône de cloche (🔔) en haut
   - Le badge devrait afficher "1" (une notification non lue)

7. **Vérifiez la Notification de Bienvenue**
   - Titre: "Bienvenue sur Maalem !"
   - Icône: 🔔 Bell en couleur cyan
   - Fond: Bleu clair (notification non lue)
   - Message: Personnalisé selon votre type (artisan/client)
   - Temps: "À l'instant" ou "Il y a X min"

---

## ✅ Vérifications à Faire

### Dans le Panneau de Notifications

- [ ] La notification de bienvenue est visible
- [ ] L'icône est une cloche (Bell) en cyan
- [ ] Le titre est "Bienvenue sur Maalem !"
- [ ] Le message est personnalisé selon le type d'utilisateur
- [ ] Le fond est bleu clair (non lue)
- [ ] Le badge affiche "1" notification non lue

### Dans la Console du Navigateur (F12 - Network)

- [ ] Requête GET vers `/api/notifications/` réussie
- [ ] Status: 200 OK
- [ ] Response contient un tableau avec votre notification
- [ ] Le champ `notification_type` est "welcome"
- [ ] Le champ `is_read` est false

### Test de l'Interaction

1. **Cliquer sur la notification**
   - [ ] Le fond passe de bleu clair à blanc
   - [ ] Le badge passe de "1" à disparaît
   - [ ] Dans Network: Requête POST vers `/api/notifications/{id}/mark_as_read/`

2. **Fermer et rouvrir le panneau**
   - [ ] La notification est toujours là mais marquée comme lue (fond blanc)

3. **Test "Effacer tout"**
   - [ ] Cliquer sur "Effacer tout"
   - [ ] Le panneau affiche "Aucune notification pour le moment."
   - [ ] Dans Network: Requête DELETE vers `/api/notifications/delete_all/`

---

## 🐛 Dépannage

### Problème: La notification n'apparaît pas

**Solution 1**: Vérifiez la console du navigateur (F12)
```javascript
// Erreur possible: Failed to fetch
// Solution: Vérifiez que le backend est en cours d'exécution
```

**Solution 2**: Vérifiez les requêtes Network
```
1. Allez dans F12 → Network
2. Filtrez par "notifications"
3. Vérifiez que GET /api/notifications/ retourne 200 OK
4. Cliquez sur la requête et vérifiez la Response
```

**Solution 3**: Vérifiez dans la base de données
```powershell
cd "C:\Users\Igolan\Desktop\site maalem\maalem-backend"
python manage.py shell
```
```python
from notifications.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

# Trouvez votre utilisateur
user = User.objects.latest('id')
print(f"Dernier utilisateur: {user.username}")

# Vérifiez ses notifications
notifications = Notification.objects.filter(recipient=user)
print(f"Nombre de notifications: {notifications.count()}")

# Affichez la notification de bienvenue
welcome = notifications.filter(notification_type='welcome').first()
if welcome:
    print(f"Type: {welcome.notification_type}")
    print(f"Texte: {welcome.text}")
    print(f"Lue: {welcome.is_read}")
else:
    print("❌ Aucune notification de bienvenue trouvée!")
```

### Problème: CORS Error

Si vous voyez une erreur CORS dans la console:
```
Access to fetch at 'http://192.168.68.58:8000/api/notifications/' has been blocked by CORS
```

**Solution**:
1. Vérifiez que le backend est bien redémarré
2. Vérifiez `settings.py` CORS_ALLOWED_ORIGINS inclut votre URL
3. Redémarrez le serveur backend

### Problème: 401 Unauthorized

Si vous obtenez une erreur 401:
```
GET /api/notifications/ 401 Unauthorized
```

**Solution**:
1. Vous n'êtes pas connecté
2. Déconnectez-vous et reconnectez-vous
3. Vérifiez que le token est stocké dans localStorage:
   ```javascript
   // Dans la console du navigateur (F12)
   console.log(localStorage.getItem('authToken'));
   // Devrait afficher un token JWT
   ```

---

## 📊 Test Avancé - Polling Automatique

### Tester le Rafraîchissement Automatique

1. **Gardez le panneau de notifications ouvert**
2. **Ouvrez F12 → Network**
3. **Attendez 30 secondes**
4. **Vérification**: Vous devriez voir une nouvelle requête GET vers `/api/notifications/`
5. **Répétez**: Toutes les 30 secondes, une nouvelle requête devrait apparaître

### Tester avec Plusieurs Notifications

Si vous voulez tester avec plusieurs notifications:

```python
# Dans le shell Django (python manage.py shell)
from notifications.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.latest('id')

# Créer une notification système
Notification.objects.create(
    recipient=user,
    notification_type='system',
    text='Ceci est une notification de test système',
    sender=None
)

print("✅ Notification de test créée!")
```

Ensuite, dans le navigateur:
- Attendez 30 secondes (polling)
- OU fermez et rouvrez le panneau de notifications
- Vous devriez voir 2 notifications maintenant

---

## 📸 Capture d'Écran Attendue

Le panneau de notifications devrait ressembler à ceci:

```
┌─────────────────────────────────────────┐
│ 🔔 Notifications                    [1] │
├─────────────────────────────────────────┤
│ [Tout marquer lu] [Effacer tout]        │
├─────────────────────────────────────────┤
│                                         │
│  🔔  Bienvenue sur Maalem !             │
│      Bienvenue sur Maalem, [Prénom] !   │
│      Félicitations pour votre ...       │
│      À l'instant                        │
│  ●  (point bleu = non lue)              │
│                                         │
└─────────────────────────────────────────┘
```

Avec:
- Icône 🔔 en cyan
- Fond bleu clair
- Badge rouge avec "1"
- Petit point bleu à droite de l'avatar

---

## ✅ Succès !

Si tout fonctionne:
- ✅ La notification de bienvenue apparaît après l'inscription
- ✅ L'icône et la couleur sont correctes
- ✅ Le message est personnalisé
- ✅ Les interactions fonctionnent (cliquer, marquer comme lu, effacer)
- ✅ Le polling automatique fonctionne

**Félicitations ! Le système de notifications est opérationnel !** 🎉

---

## 📝 Notes

1. **Persistance**: Les notifications sont stockées dans la base de données PostgreSQL
2. **Temps réel**: Le polling toutes les 30 secondes est un bon compromis
3. **Performance**: Pour beaucoup d'utilisateurs, envisager WebSockets
4. **Notifications futures**: Le système est prêt pour d'autres types de notifications

---

**Besoin d'aide?** Vérifiez les logs du serveur backend et la console du navigateur pour plus de détails sur les erreurs.

# Intégration des Notifications Backend-Frontend
**Date**: 2025-10-19

## 🎯 Objectif
Connecter le panneau de notifications du frontend à l'API backend pour afficher les vraies notifications, incluant la notification de bienvenue.

---

## 📋 Modifications Effectuées

### 1. **Nouveau Service de Notifications** ✅
**Fichier**: `maalem-frontend/src/services/notifications.js`

**Création d'un service complet pour gérer les notifications**:
- ✅ `getNotifications()` - Récupère toutes les notifications de l'utilisateur
- ✅ `markNotificationAsRead(id)` - Marque une notification comme lue
- ✅ `markAllNotificationsAsRead()` - Marque toutes les notifications comme lues
- ✅ `deleteAllNotifications()` - Supprime toutes les notifications
- ✅ `getNotificationTitle()` - Génère des titres appropriés selon le type
- ✅ `formatNotificationTime()` - Formate l'heure de manière lisible

**Types de notifications supportés**:
- `welcome` - Notification de bienvenue (avec icône Bell cyan)
- `message` - Messages privés
- `comment` - Commentaires
- `like` - J'aime
- `follow` - Nouveaux abonnés
- `new_post` - Nouvelles publications
- `system` - Notifications système

---

### 2. **Mise à Jour du Layout** ✅
**Fichier**: `maalem-frontend/src/components/Layout.jsx`

**Changements**:
- ❌ **Supprimé**: Stockage des notifications dans `localStorage`
- ✅ **Ajouté**: Récupération des notifications depuis l'API backend
- ✅ **Ajouté**: Polling automatique toutes les 30 secondes pour les nouvelles notifications
- ✅ **Ajouté**: Importation du service `getNotifications`

**Code ajouté**:
```javascript
// Fetch notifications from backend
useEffect(() => {
  const fetchNotifications = async () => {
    if (isAuthenticatedState) {
      try {
        const fetchedNotifications = await getNotifications();
        setNotifications(fetchedNotifications);
      } catch (error) {
        console.error('Error fetching notifications:', error);
      }
    }
  };
  
  fetchNotifications();
  
  // Poll for new notifications every 30 seconds if authenticated
  let interval;
  if (isAuthenticatedState) {
    interval = setInterval(fetchNotifications, 30000);
  }
  
  return () => {
    if (interval) clearInterval(interval);
  };
}, [isAuthenticatedState]);
```

---

### 3. **Mise à Jour du Panneau de Notifications** ✅
**Fichier**: `maalem-frontend/src/components/NotificationPanel.jsx`

**Changements**:
- ✅ Importation des icônes supplémentaires: `Heart`, `UserPlus`, `FileText`, `AlertCircle`
- ✅ Importation du service de notifications au lieu de utils.js
- ✅ Ajout du support pour le type `welcome` avec icône Bell cyan
- ✅ Ajout du support pour le type `system` avec icône AlertCircle orange
- ✅ Ajout du support pour `comment` et `like` avec icônes appropriées

**Nouveaux types d'icônes**:
```javascript
case 'welcome': return <Bell className="w-4 h-4 text-cyan-500" />;
case 'comment': return <MessageCircle className="w-4 h-4 text-blue-500" />;
case 'like': return <Heart className="w-4 h-4 text-red-500" />;
case 'follow': return <UserPlus className="w-4 h-4 text-green-500" />;
case 'new_post': return <FileText className="w-4 h-4 text-purple-500" />;
case 'system': return <AlertCircle className="w-4 h-4 text-orange-500" />;
```

---

### 4. **Nettoyage de utils.js** ✅
**Fichier**: `maalem-frontend/src/lib/utils.js`

**Changements**:
- ❌ **Supprimé**: Fonctions de notification simulées (mock)
- ✅ **Conservé**: Uniquement la fonction utilitaire `cn()` pour les classes CSS

Les fonctions suivantes ont été déplacées vers `services/notifications.js` avec des vraies implémentations API:
- `markNotificationAsRead()`
- `markAllNotificationsAsRead()`
- `deleteAllNotifications()`

---

### 5. **Backend - Ajout de l'Endpoint Delete All** ✅
**Fichier**: `maalem-backend/maalem/notifications/views.py`

**Nouveau endpoint ajouté**:
```python
@action(detail=False, methods=['delete'])
def delete_all(self, request):
    count = self.get_queryset().count()
    self.get_queryset().delete()
    return Response({'status': f'{count} notifications deleted'})
```

**URL**: `DELETE /api/notifications/delete_all/`

---

### 6. **Backend - Amélioration du Serializer** ✅
**Fichier**: `maalem-backend/maalem/notifications/serializers.py`

**Changements**:
- ✅ Gestion du cas où `sender` est `None` (notifications système/bienvenue)
- ✅ Ajout du champ `first_name` dans les données du sender
- ✅ Protection contre les erreurs si sender est null

```python
def get_sender(self, obj):
    if obj.sender:
        return {
            'id': obj.sender.id,
            'username': obj.sender.username,
            'first_name': obj.sender.first_name,
            'profile_picture': obj.sender.profile_picture.url if obj.sender.profile_picture else None
        }
    return None
```

---

## 🔄 Flux de Données

### Inscription d'un Nouvel Utilisateur
```
1. Utilisateur s'inscrit via AuthModal
2. Backend crée l'utilisateur
3. Signal post_save se déclenche (signals.py)
4. Création de notification de bienvenue (NotificationService)
5. Notification enregistrée en BDD (type='welcome', sender=None)
6. Frontend polling récupère la notification via API
7. Notification apparaît dans NotificationPanel avec icône Bell cyan
```

### Affichage des Notifications
```
1. Layout.jsx charge les notifications au montage
2. getNotifications() appelle /api/notifications/
3. Backend retourne les notifications de l'utilisateur
4. Service transforme les données pour le frontend
5. NotificationPanel affiche avec icône et formatage appropriés
6. Polling toutes les 30 secondes pour nouvelles notifications
```

---

## 📡 Endpoints API Utilisés

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/notifications/` | GET | Récupérer toutes les notifications |
| `/api/notifications/{id}/mark_as_read/` | POST | Marquer une notification comme lue |
| `/api/notifications/mark_all_as_read/` | POST | Marquer toutes comme lues |
| `/api/notifications/delete_all/` | DELETE | Supprimer toutes les notifications |

---

## 🎨 Types de Notifications et Icônes

| Type | Titre | Icône | Couleur |
|------|-------|-------|---------|
| `welcome` | "Bienvenue sur Maalem !" | Bell | Cyan |
| `message` | "{sender} vous a envoyé un message" | MessageCircle | Bleu |
| `comment` | "{sender} a commenté" | MessageCircle | Bleu |
| `like` | "{sender} a aimé" | Heart | Rouge |
| `follow` | "{sender} vous suit" | UserPlus | Vert |
| `new_post` | "{sender} a publié" | FileText | Violet |
| `system` | "Notification système" | AlertCircle | Orange |

---

## ✅ Fonctionnalités Implémentées

1. ✅ **Récupération des notifications** depuis le backend
2. ✅ **Affichage de la notification de bienvenue** dans le panneau
3. ✅ **Polling automatique** toutes les 30 secondes
4. ✅ **Marquer comme lu** - une notification
5. ✅ **Marquer tout comme lu** - toutes les notifications
6. ✅ **Effacer tout** - supprimer toutes les notifications
7. ✅ **Formatage du temps** relatif (il y a X min/h/j)
8. ✅ **Icônes différenciées** par type de notification
9. ✅ **Gestion des notifications système** sans sender
10. ✅ **Badge de compteur** de notifications non lues

---

## 🧪 Test

### Tester la Notification de Bienvenue
1. Assurez-vous que le backend est démarré
2. Assurez-vous que le frontend est démarré
3. Ouvrez la console du navigateur (F12)
4. Déconnectez-vous si vous êtes connecté
5. Inscrivez-vous avec un nouveau compte (email unique)
6. Attendez la fin de l'inscription
7. Cliquez sur l'icône de notification (Bell)
8. Vous devriez voir "Bienvenue sur Maalem !" avec icône cyan

### Vérifier le Polling
1. Gardez le panneau de notifications ouvert
2. Ouvrez la console développeur (F12) → Onglet Network
3. Attendez 30 secondes
4. Vous devriez voir une requête GET vers `/api/notifications/`

---

## 🔧 Configuration Requise

### Frontend
- Axios ou Fetch API configuré avec `VITE_API_URL`
- Token d'authentification stocké dans `localStorage.authToken`

### Backend
- Django REST Framework installé
- CORS configuré pour autoriser le frontend
- Endpoints notifications enregistrés dans les URLs

---

## 📝 Notes Importantes

1. **Notifications Temps Réel**: Actuellement, le système utilise le polling (30s). Pour du temps réel via WebSockets, le backend a déjà la structure prête avec Django Channels.

2. **Performance**: Le polling toutes les 30 secondes est un bon compromis. Pour des apps avec beaucoup d'utilisateurs, envisager WebSockets.

3. **Gestion des Erreurs**: Si l'API échoue, les notifications ne seront pas affichées mais l'app continue de fonctionner.

4. **Authentification**: Les notifications ne sont récupérées que si l'utilisateur est authentifié.

---

## 🚀 Prochaines Améliorations Possibles

1. ⚡ **WebSocket en temps réel** - Au lieu du polling
2. 🔔 **Notifications navigateur** - API Notification du navigateur
3. 🎵 **Son de notification** - Alert audio pour nouvelles notifications
4. 📱 **Push notifications** - Pour notifications mobiles
5. 🔍 **Filtres** - Filtrer par type de notification
6. 📊 **Pagination** - Pour utilisateurs avec beaucoup de notifications
7. ⏰ **Notifications programmées** - Rappels, etc.

---

## ✅ Résumé des Fichiers Modifiés

### Frontend
1. ✅ **CRÉÉ**: `src/services/notifications.js`
2. ✅ **MODIFIÉ**: `src/components/Layout.jsx`
3. ✅ **MODIFIÉ**: `src/components/NotificationPanel.jsx`
4. ✅ **MODIFIÉ**: `src/lib/utils.js`

### Backend
1. ✅ **MODIFIÉ**: `maalem/notifications/views.py`
2. ✅ **MODIFIÉ**: `maalem/notifications/serializers.py`

---

**Système de notifications fonctionnel et connecté au backend !** 🎉

# User Model Improvements - Documentation
**Date**: 2025-10-19

## 🎯 Objectifs

Cette mise à jour améliore le modèle User avec les fonctionnalités suivantes :

1. ✅ **Affichage "Membre depuis"** avec temps relatif (hier, une semaine, 2 semaines, un mois, un an, etc.)
2. ✅ **Suppression de la colonne username** - Les noms sont stockés dans `first_name` et `last_name`
3. ✅ **Email comme identifiant principal** (mais `username` reste pour compatibilité Django)
4. ✅ **Champ de vérification** `is_verified` pour marquer les comptes vérifiés par l'admin

---

## 📋 Modifications Backend

### 1. **Modèle User** (`users/models.py`)

#### Changements:
- ✅ Ajout du champ `is_verified` (BooleanField, default=False)
- ✅ Ajout de la méthode `__str__()` pour afficher le nom complet et l'email
- ✅ Conservation de `username` pour compatibilité Django (généré automatiquement)

**Code ajouté**:
```python
# Verification field to mark verified accounts
is_verified = models.BooleanField(
    default=False,
    help_text='Designates whether this user account has been verified by admin.'
)

def __str__(self):
    return f"{self.get_full_name()} ({self.email})"
```

**Note**: Le `username` reste présent mais est généré automatiquement à partir de l'email. Django Auth nécessite un USERNAME_FIELD unique, donc nous gardons `username` mais utilisons `email` pour l'authentification via le backend personnalisé.

---

### 2. **Serializers** (`users/serializers.py`)

#### UserSerializer
**Champs ajoutés**:
- `first_name` (prénom)
- `last_name` (nom de famille)
- `is_verified` (lecture seule)
- `date_joined` (lecture seule)

```python
fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_type', 
         'phone_number', 'address', 'profile_picture', 'bio', 'specialty', 
         'experience_years', 'rating', 'latitude', 'longitude', 'is_verified', 
         'date_joined']
read_only_fields = ['rating', 'is_verified', 'date_joined']
```

#### UserRegistrationSerializer
**Champs modifiés**:
- ❌ Supprimé: `username` (généré automatiquement)
- ✅ Ajouté: `first_name` (requis)
- ✅ Ajouté: `last_name` (requis)

**Validations ajoutées**:
```python
if not attrs.get('first_name'):
    raise serializers.ValidationError({"first_name": "Le prénom est requis."})
if not attrs.get('last_name'):
    raise serializers.ValidationError({"last_name": "Le nom de famille est requis."})
```

#### UserUpdateSerializer
**Champs ajoutés**:
- `first_name`
- `last_name`

---

### 3. **Admin Panel** (`users/admin.py`) ✅ NOUVEAU FICHIER

Création d'un panneau d'administration complet pour gérer les utilisateurs:

**Fonctionnalités**:
- ✅ Liste affichant: email, prénom, nom, type, statut vérifié, staff, date d'inscription
- ✅ Filtres: type d'utilisateur, vérifié, staff, superuser, actif
- ✅ Recherche: email, prénom, nom, username
- ✅ Organisation: par date d'inscription (plus récent en premier)
- ✅ **Actions en masse**: "Marquer comme vérifié" / "Marquer comme non vérifié"

**Sections du formulaire**:
1. **None**: username, email, password
2. **Personal info**: prénom, nom, téléphone, bio
3. **User Type**: type d'utilisateur, vérifié ✅
4. **Artisan Info**: spécialité, expérience, rating, adresse, coordonnées
5. **Permissions**: actif, staff, superuser, groupes
6. **Important dates**: dernière connexion, date d'inscription
7. **Profile**: photo de profil

**Actions personnalisées**:
```python
def verify_users(self, request, queryset):
    """Mark selected users as verified"""
    updated = queryset.update(is_verified=True)
    self.message_user(request, f'{updated} utilisateur(s) marqué(s) comme vérifié(s).')

def unverify_users(self, request, queryset):
    """Mark selected users as unverified"""
    updated = queryset.update(is_verified=False)
    self.message_user(request, f'{updated} utilisateur(s) marqué(s) comme non vérifié(s).')
```

---

### 4. **Migration** (`0004_add_is_verified_field.py`)

**Commande utilisée**:
```bash
python manage.py makemigrations users --name add_is_verified_field
python manage.py migrate users
```

**Changements en base de données**:
- ✅ Ajout de la colonne `is_verified` (BOOLEAN, DEFAULT FALSE)

---

## 📋 Modifications Frontend

### 1. **Utilitaire de formatage** (`lib/utils.js`)

Ajout de la fonction `formatMemberSince()` pour afficher le temps relatif:

```javascript
/**
 * Format a date to relative time in French
 * @param {string|Date} dateString - The date to format
 * @returns {string} - Formatted relative time in French
 */
export function formatMemberSince(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now - date;
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  const diffWeeks = Math.floor(diffDays / 7);
  const diffMonths = Math.floor(diffDays / 30);
  const diffYears = Math.floor(diffDays / 365);
  
  if (diffDays === 0) return "Aujourd'hui";
  if (diffDays === 1) return "Hier";
  if (diffDays < 7) return `${diffDays} jours`;
  if (diffWeeks === 1) return "Une semaine";
  if (diffWeeks < 4) return `${diffWeeks} semaines`;
  if (diffMonths === 1) return "Un mois";
  if (diffMonths < 12) return `${diffMonths} mois`;
  if (diffYears === 1) return "Un an";
  return `${diffYears} ans`;
}
```

**Exemples de sortie**:
- Inscrit aujourd'hui → "Aujourd'hui"
- Inscrit hier → "Hier"
- Inscrit il y a 5 jours → "5 jours"
- Inscrit il y a 1 semaine → "Une semaine"
- Inscrit il y a 3 semaines → "3 semaines"
- Inscrit il y a 1 mois → "Un mois"
- Inscrit il y a 6 mois → "6 mois"
- Inscrit il y a 1 an → "Un an"
- Inscrit il y a 3 ans → "3 ans"

---

### 2. **UserAccountModal** (`components/UserAccountModal.jsx`)

#### Importation de la fonction:
```javascript
import { formatMemberSince } from '@/lib/utils';
```

#### State mis à jour:
```javascript
const [userData, setUserData] = useState({
  firstName: "",
  lastName: "",
  email: "",
  phone: "",
  isVerified: false, // ✅ Nouveau champ
  // ... autres champs
});
```

#### Récupération du profil:
```javascript
setUserData({
  firstName: profile.first_name || profile.username.split(' ')[0] || '',
  lastName: profile.last_name || profile.username.split(' ')[1] || '',
  email: profile.email,
  phone: profile.phone_number || '',
  isVerified: profile.is_verified || false, // ✅ Nouveau
  // ...
  memberSince: profile.date_joined, // ✅ Date complète au lieu de juste l'année
});
```

#### Affichage "Membre depuis":
```javascript
<div className="flex items-center gap-2">
  <Calendar className="w-4 h-4" />
  <span>
    Membre depuis {userData.memberSince ? formatMemberSince(userData.memberSince) : 'Non renseigné'}
  </span>
</div>
```

**Avant**: "Membre depuis 2024"
**Après**: "Membre depuis 3 semaines" (exemple)

#### Badge "Profil vérifié" (conditionnel):
```javascript
{userData.isVerified && (
  <Badge className="mt-3 bg-green-100 text-green-800">
    Profil {currentUserType === 'client' ? 'Client' : 'Artisan'} vérifié
  </Badge>
)}
```

**Comportement**:
- ✅ Affiché uniquement si `is_verified = true`
- ❌ Masqué si `is_verified = false`

---

## 🔄 Flux de Données

### Inscription d'un nouvel utilisateur

```
1. Frontend envoie: {
     email: "user@example.com",
     first_name: "Jean",
     last_name: "Dupont",
     password: "****",
     user_type: "client"
   }

2. Backend crée User avec:
   - email: "user@example.com"
   - first_name: "Jean"
   - last_name: "Dupont"
   - username: "user_c" (généré auto)
   - is_verified: false (par défaut)
   - date_joined: 2025-10-19T10:30:00Z

3. Frontend reçoit:
   {
     id: 123,
     email: "user@example.com",
     first_name: "Jean",
     last_name: "Dupont",
     is_verified: false,
     date_joined: "2025-10-19T10:30:00Z",
     ...
   }

4. Frontend affiche:
   - Nom: "Jean Dupont"
   - Email: "user@example.com"
   - Membre depuis: "Aujourd'hui"
   - Badge vérifié: ❌ (masqué car is_verified=false)
```

---

### Vérification par l'admin

```
1. Admin ouvre Django Admin (/admin/)
2. Va dans "Users"
3. Sélectionne l'utilisateur "Jean Dupont"
4. Clique sur "Marquer comme vérifié" (action en masse)
   OU
   Ouvre l'utilisateur et coche "Is verified"
5. Sauvegarde

6. is_verified passe à True en base de données

7. Utilisateur recharge sa page de profil
8. Badge "Profil vérifié" apparaît ✅
```

---

## 🧪 Comment Tester

### Test 1: Inscription d'un nouvel utilisateur

1. **Ouvrir le site**: http://192.168.68.58:5173
2. **S'inscrire** avec:
   - Prénom: Test
   - Nom: Utilisateur
   - Email: test@example.com (unique)
   - Type: Client
   - Mot de passe: TestPass123!
3. **Vérifier**:
   - ✅ Inscription réussie
   - ✅ Connexion automatique
4. **Aller dans "Mon Compte"**
5. **Vérifier l'affichage**:
   - Nom: "Test Utilisateur"
   - Membre depuis: "Aujourd'hui"
   - Badge vérifié: ❌ (absent)

---

### Test 2: Vérification d'un compte par l'admin

1. **Ouvrir Django Admin**: http://192.168.68.58:8000/admin/
2. **Se connecter** avec compte superuser
3. **Aller dans "Users"**
4. **Trouver l'utilisateur** "Test Utilisateur"
5. **Méthode 1 - Action en masse**:
   - Cocher la case de l'utilisateur
   - Sélectionner "Marquer comme vérifié" dans le menu déroulant
   - Cliquer sur "Go"
   - Message: "1 utilisateur(s) marqué(s) comme vérifié(s)."
6. **Méthode 2 - Formulaire d'édition**:
   - Cliquer sur l'utilisateur
   - Cocher "Is verified"
   - Cliquer sur "Save"
7. **Retourner sur le site** (frontend)
8. **Rafraîchir la page du compte**
9. **Vérifier**:
   - ✅ Badge "Profil Client vérifié" apparaît
   - ✅ Fond vert clair avec texte vert

---

### Test 3: Temps relatif "Membre depuis"

Pour tester les différentes durées, modifier manuellement en base:

```sql
-- Dans PostgreSQL
UPDATE users_user 
SET date_joined = NOW() - INTERVAL '1 day' 
WHERE email = 'test@example.com';
-- Résultat attendu: "Hier"

UPDATE users_user 
SET date_joined = NOW() - INTERVAL '7 days' 
WHERE email = 'test@example.com';
-- Résultat attendu: "Une semaine"

UPDATE users_user 
SET date_joined = NOW() - INTERVAL '21 days' 
WHERE email = 'test@example.com';
-- Résultat attendu: "3 semaines"

UPDATE users_user 
SET date_joined = NOW() - INTERVAL '1 month' 
WHERE email = 'test@example.com';
-- Résultat attendu: "Un mois"

UPDATE users_user 
SET date_joined = NOW() - INTERVAL '6 months' 
WHERE email = 'test@example.com';
-- Résultat attendu: "6 mois"

UPDATE users_user 
SET date_joined = NOW() - INTERVAL '1 year' 
WHERE email = 'test@example.com';
-- Résultat attendu: "Un an"

UPDATE users_user 
SET date_joined = NOW() - INTERVAL '3 years' 
WHERE email = 'test@example.com';
-- Résultat attendu: "3 ans"
```

---

## 📊 Structure de la Table `users_user`

### Colonnes principales:

| Colonne | Type | Description | Modifiable par user |
|---------|------|-------------|---------------------|
| `id` | INT | ID unique | ❌ |
| `username` | VARCHAR(150) | Généré auto (ex: "user_c") | ❌ |
| `email` | VARCHAR(254) | Identifiant de connexion | ✅ |
| `first_name` | VARCHAR(150) | Prénom | ✅ |
| `last_name` | VARCHAR(150) | Nom de famille | ✅ |
| `user_type` | VARCHAR(10) | "client" ou "artisan" | ❌ |
| `is_verified` | BOOLEAN | Vérifié par admin | ❌ (admin only) |
| `date_joined` | TIMESTAMP | Date d'inscription | ❌ |
| `phone_number` | VARCHAR(15) | Téléphone | ✅ |
| `address` | TEXT | Adresse | ✅ |
| `bio` | TEXT | Biographie | ✅ |
| `specialty` | VARCHAR(100) | Spécialité (artisans) | ✅ |
| `rating` | DECIMAL(3,2) | Note (artisans) | ❌ |

---

## ✅ Résumé des Fichiers Modifiés

### Backend
1. ✅ **MODIFIÉ**: `maalem/users/models.py` - Ajout `is_verified`, `__str__()`
2. ✅ **MODIFIÉ**: `maalem/users/serializers.py` - Ajout first_name, last_name, is_verified, date_joined
3. ✅ **CRÉÉ**: `maalem/users/admin.py` - Panneau admin complet
4. ✅ **CRÉÉ**: `maalem/users/migrations/0004_add_is_verified_field.py` - Migration

### Frontend
1. ✅ **MODIFIÉ**: `src/lib/utils.js` - Fonction `formatMemberSince()`
2. ✅ **MODIFIÉ**: `src/components/UserAccountModal.jsx` - Affichage temps relatif et badge vérifié

---

## 🎯 Avantages de ces Modifications

1. **UX Améliorée**: 
   - "Membre depuis 2 semaines" est plus lisible que "Membre depuis 2024"
   - Badge de vérification augmente la confiance

2. **Meilleure Gestion**:
   - Les admins peuvent facilement vérifier les comptes
   - Actions en masse pour vérifier plusieurs utilisateurs

3. **Données Plus Propres**:
   - first_name et last_name séparés (meilleures requêtes)
   - Email comme identifiant principal (plus intuitif)

4. **Sécurité**:
   - Badge vérifié uniquement pour comptes approuvés
   - is_verified non modifiable par l'utilisateur

---

## 🔐 Sécurité

- ✅ Le champ `is_verified` est **read_only** dans le serializer
- ✅ Seuls les **admins** peuvent modifier `is_verified`
- ✅ Le badge n'apparaît que si `is_verified = true`
- ✅ Les utilisateurs ne peuvent pas se vérifier eux-mêmes

---

**Système de vérification et affichage "Membre depuis" complètement fonctionnel !** 🎉

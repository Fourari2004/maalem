# Guide de Test - Système d'Avis et Profils Mis à Jour

## 🎯 Ce qui a été implémenté

### 1. Page Maalems (Liste des Artisans)
- ✅ Affichage du prénom et nom complet
- ✅ Badge "✓ Vérifié" avec style vert

### 2. Profil Artisan
- ✅ Nom complet affiché
- ✅ Badge "✓ Profil vérifié" 
- ✅ Onglet "Postes" - Publications de l'artisan
- ✅ Onglet "Avis" avec:
  - Formulaire pour laisser un avis (clients seulement)
  - Liste de tous les avis reçus

### 3. Système d'Avis Complet
- ✅ Seuls les clients peuvent laisser des avis
- ✅ Un seul avis par client par artisan
- ✅ Note générale + notes détaillées
- ✅ Commentaire obligatoire
- ✅ Mise à jour automatique du rating artisan

---

## 🚀 Comment Tester

### Étape 1: Démarrer les serveurs

#### Backend Django
```powershell
cd "c:\Users\Igolan\Desktop\site maalem\maalem-backend"
python manage.py runserver
```

#### Frontend React
```powershell
cd "c:\Users\Igolan\Desktop\site maalem\maalem-frontend"
npm run dev
```

---

### Étape 2: Tester la Page Maalems

1. Ouvrir http://localhost:5173/maalems
2. **Vérifier:**
   - [ ] Les artisans affichent leur prénom et nom (pas le username)
   - [ ] Les artisans vérifiés ont un badge vert "✓ Vérifié"
   - [ ] Le badge est bien visible et stylisé

---

### Étape 3: Tester le Profil Artisan

1. Cliquer sur "Voir Profil" d'un artisan
2. **Vérifier dans l'en-tête:**
   - [ ] Nom complet affiché (prénom + nom)
   - [ ] Si vérifié: badge "✓ Profil vérifié" en vert

3. **Onglet "À propos":**
   - [ ] Description de l'artisan
   - [ ] Compétences affichées

4. **Onglet "Postes":**
   - [ ] Affiche les publications de cet artisan uniquement
   - [ ] Chaque post montre:
     - Image (si disponible)
     - Contenu (3 lignes max)
     - Nombre de likes
     - Nombre de commentaires
     - Date de publication
   - [ ] Si aucun post: message "Aucune publication pour le moment"

5. **Onglet "Avis":**
   - [ ] Voir section ci-dessous pour tests détaillés

---

### Étape 4: Tester le Système d'Avis

#### Test A: En tant que CLIENT

1. **Se connecter en tant que client**
   - Email: un compte client existant
   - Type: Client

2. **Visiter le profil d'un artisan** que vous n'avez jamais évalué

3. **Onglet "Avis" - Formulaire visible:**
   - [ ] Formulaire "Laisser un avis" affiché
   - [ ] 5 étoiles cliquables pour "Note générale"
   - [ ] 3 sections de notes détaillées:
     - Qualité du travail
     - Ponctualité
     - Professionnalisme
   - [ ] Zone de texte pour commentaire

4. **Laisser un avis:**
   - [ ] Cliquer sur 4 ou 5 étoiles (note générale)
   - [ ] Optionnel: donner des notes détaillées
   - [ ] Écrire un commentaire (exemple: "Excellent travail, très professionnel !")
   - [ ] Cliquer "Publier l'avis"

5. **Vérifier le succès:**
   - [ ] Message toast "Avis publié avec succès!"
   - [ ] Le formulaire est réinitialisé
   - [ ] Votre avis apparaît dans la liste ci-dessous
   - [ ] Le rating de l'artisan est mis à jour (en haut du profil)

6. **Tenter de laisser un 2ème avis au même artisan:**
   - [ ] Le formulaire affiche: "Vous avez déjà laissé un avis pour cet artisan"
   - [ ] Le formulaire n'est plus disponible

#### Test B: En tant qu'ARTISAN

1. **Se connecter en tant qu'artisan**
   - Email: un compte artisan existant
   - Type: Artisan

2. **Visiter le profil d'un autre artisan**

3. **Onglet "Avis":**
   - [ ] Message affiché: "Seuls les clients peuvent laisser des avis"
   - [ ] Pas de formulaire visible
   - [ ] La liste des avis est visible (lecture seule)

#### Test C: Non connecté

1. **Se déconnecter** (ou ouvrir en navigation privée)

2. **Visiter le profil d'un artisan**

3. **Onglet "Avis":**
   - [ ] Formulaire affiche "Vous devez être connecté pour laisser un avis" (ou similaire)
   - [ ] La liste des avis est visible (lecture seule)

---

### Étape 5: Vérifier la Liste des Avis

Dans l'onglet "Avis" de n'importe quel artisan:

1. **Si aucun avis:**
   - [ ] Icône utilisateur grise
   - [ ] Message: "Aucun avis pour le moment"
   - [ ] "Soyez le premier à laisser un avis !"

2. **Si des avis existent:**
   - [ ] Chaque avis affiche:
     - [ ] Photo de profil du reviewer
     - [ ] Nom du reviewer
     - [ ] Date de l'avis (format français: "19 octobre 2025")
     - [ ] Étoiles de notation (remplies en jaune)
     - [ ] Badge avec la note (ex: "4/5")
     - [ ] Commentaire complet
     - [ ] Section "Détails" avec:
       - Qualité du travail (si fournie)
       - Ponctualité (si fournie)
       - Professionnalisme (si fourni)

---

## 🐛 Problèmes Potentiels et Solutions

### Problème 1: "Aucun artisan trouvé"
**Solution:** 
```powershell
cd maalem-backend
python manage.py create_sample_data
```

### Problème 2: Erreur 401 (Non autorisé) lors de la création d'avis
**Cause:** Token expiré ou non connecté
**Solution:** 
- Se déconnecter et se reconnecter
- Vérifier que vous êtes connecté en tant que CLIENT

### Problème 3: "Seuls les clients peuvent laisser des avis"
**Cause:** Connecté en tant qu'artisan
**Solution:** 
- Se déconnecter
- Se connecter avec un compte CLIENT

### Problème 4: Les posts ne s'affichent pas
**Cause:** L'artisan n'a pas encore publié de posts
**Solution:** 
- Se connecter en tant qu'artisan
- Créer un post via "Créer un post"
- Vérifier que le post apparaît dans le profil

### Problème 5: Backend non connecté
**Erreur:** `Failed to fetch` ou `Network error`
**Solution:**
```powershell
# Vérifier que le backend tourne
cd "c:\Users\Igolan\Desktop\site maalem\maalem-backend"
python manage.py runserver

# Devrait afficher:
# Starting development server at http://127.0.0.1:8000/
```

---

## 📊 Vérifications Backend (API)

### Test API avec curl ou Postman:

#### 1. Obtenir les avis d'un artisan
```bash
GET http://localhost:8000/api/reviews/?artisan=1
```

#### 2. Créer un avis (nécessite authentification)
```bash
POST http://localhost:8000/api/reviews/
Headers: Authorization: Bearer {votre_token}
Body: {
  "artisan": 1,
  "rating": 5,
  "comment": "Excellent travail !",
  "work_quality": 5,
  "punctuality": 4,
  "professionalism": 5
}
```

#### 3. Vérifier si on peut reviewer
```bash
GET http://localhost:8000/api/reviews/can_review/?artisan_id=1
Headers: Authorization: Bearer {votre_token}
```

#### 4. Obtenir tous les posts
```bash
GET http://localhost:8000/api/posts/
```

---

## ✅ Checklist Complète

### Interface Utilisateur
- [ ] Badge vérifié affiché sur page Maalems
- [ ] Badge vérifié affiché sur profil artisan
- [ ] Nom complet affiché (prénom + nom)
- [ ] Onglet "Postes" fonctionnel
- [ ] Onglet "Avis" fonctionnel

### Formulaire d'Avis
- [ ] Formulaire visible pour clients uniquement
- [ ] Note générale obligatoire
- [ ] Commentaire obligatoire
- [ ] Notes détaillées optionnelles
- [ ] Validation avant soumission
- [ ] Message de succès après soumission
- [ ] Formulaire réinitialisé après succès

### Restrictions
- [ ] Un seul avis par client par artisan
- [ ] Artisans ne peuvent pas laisser d'avis
- [ ] Non connectés ne peuvent pas laisser d'avis

### Affichage des Avis
- [ ] Liste de tous les avis visible pour tous
- [ ] Étoiles correctement affichées
- [ ] Photos de profil affichées
- [ ] Dates formatées en français
- [ ] Notes détaillées affichées

### Intégration
- [ ] Rating artisan mis à jour après avis
- [ ] Posts d'artisan filtrés correctement
- [ ] Pas d'erreurs dans la console

---

## 📝 Notes

- **Backend**: Toutes les API sont déjà prêtes (créées dans la session précédente)
- **Frontend**: Tous les composants sont créés et intégrés
- **Service**: `reviews.js` contient toutes les fonctions d'API nécessaires
- **Permissions**: Gérées côté backend ET frontend pour double sécurité

---

**Date:** 2025-10-19
**Statut:** ✅ Prêt pour test

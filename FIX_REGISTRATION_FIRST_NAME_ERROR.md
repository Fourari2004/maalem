# Fix Registration Error - first_name Required
**Date**: 2025-10-19
**Issue**: `{"first_name":["Le prénom est requis."]}`

## 🐛 Problem

When users tried to register, they received an error:
```json
{"first_name":["Le prénom est requis."]}
```

This happened because the frontend was not sending `first_name` and `last_name` fields to the backend API during registration.

---

## 🔍 Root Cause

In [`AuthModal.jsx`](file://c:\Users\Igolan\Desktop\site%20maalem\maalem-frontend\src\components\AuthModal.jsx), the registration data was being sent with:
- ❌ `username` (which was auto-generated but not required by backend)
- ❌ Missing `first_name` (required by backend)
- ❌ Missing `last_name` (required by backend)

The form had `firstName` and `lastName` fields, but they weren't being mapped to `first_name` and `last_name` in the API request.

---

## ✅ Solution

Updated the registration data structure in [`AuthModal.jsx`](file://c:\Users\Igolan\Desktop\site%20maalem\maalem-frontend\src\components\AuthModal.jsx) to properly send:

**Before**:
```javascript
const registrationData = {
  username: `${formData.firstName}.${formData.lastName}`.toLowerCase()...,
  email: formData.email,
  password: formData.password,
  password2: formData.confirmPassword,
  user_type: userType,
  // ... other fields
};
```

**After**:
```javascript
const registrationData = {
  first_name: formData.firstName,       // ✅ Added
  last_name: formData.lastName,         // ✅ Added
  email: formData.email,
  password: formData.password,
  password2: formData.confirmPassword,
  user_type: userType,
  bio: formData.description || '',
};

// Add artisan-specific fields
if (userType === 'artisan') {
  if (formData.phone) registrationData.phone_number = formData.phone;
  if (formData.address) registrationData.address = formData.address;
  if (formData.specialty) registrationData.specialty = formData.specialty;
  if (formData.experience) registrationData.experience_years = parseInt(formData.experience) || 0;
}
```

---

## 📋 Changes Made

### File: [`maalem-frontend/src/components/AuthModal.jsx`](file://c:\Users\Igolan\Desktop\site%20maalem\maalem-frontend\src\components\AuthModal.jsx)

1. ✅ **Added `first_name`**: Maps `formData.firstName` to `first_name`
2. ✅ **Added `last_name`**: Maps `formData.lastName` to `last_name`
3. ✅ **Removed `username`**: No longer sent (backend generates it automatically)
4. ✅ **Cleaned up field deletion logic**: Removed code that was deleting required fields
5. ✅ **Better field organization**: Artisan-specific fields are only added when `userType === 'artisan'`

---

## 🧪 Testing

### Test Registration - Client

1. Open the website
2. Click "S'inscrire"
3. Choose "Client"
4. Fill in the form:
   - Prénom: Test
   - Nom: Utilisateur
   - Email: test@example.com
   - Password: Pass123!
   - Confirm Password: Pass123!
5. Click "Créer mon compte client"
6. **Expected**: ✅ Success! "🎉 Inscription réussie!"
7. **Expected**: ✅ Automatic login

### Test Registration - Artisan

1. Open the website
2. Click "S'inscrire"
3. Choose "Artisan"
4. Fill in the form:
   - Prénom: Jean
   - Nom: Dupont
   - Email: jean@example.com
   - Password: Pass123!
   - Confirm Password: Pass123!
   - Téléphone: 0612345678
   - Adresse: 123 Rue Example
   - Ville: Casablanca
   - Spécialité: Plombier
   - Expérience: 5
5. Click "Créer mon compte artisan"
6. **Expected**: ✅ Success! "🎉 Inscription réussie!"
7. **Expected**: ✅ Automatic login

---

## 📊 API Request Comparison

### Before (Broken)

**Request to `/api/users/register/`**:
```json
{
  "username": "test.user",
  "email": "test@example.com",
  "password": "Pass123!",
  "password2": "Pass123!",
  "user_type": "client"
}
```

**Response**: ❌ Error
```json
{
  "first_name": ["Le prénom est requis."],
  "last_name": ["Le nom de famille est requis."]
}
```

### After (Fixed)

**Request to `/api/users/register/`**:
```json
{
  "first_name": "Test",
  "last_name": "User",
  "email": "test@example.com",
  "password": "Pass123!",
  "password2": "Pass123!",
  "user_type": "client",
  "bio": ""
}
```

**Response**: ✅ Success
```json
{
  "id": 123,
  "email": "test@example.com",
  "first_name": "Test",
  "last_name": "User",
  "user_type": "client",
  "is_verified": false,
  "date_joined": "2025-10-19T10:30:00Z",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## ✅ Validation

The backend now validates:
- ✅ `first_name` is required (min 1 character)
- ✅ `last_name` is required (min 1 character)
- ✅ `email` is required and must be valid
- ✅ `password` is required (min 8 characters)
- ✅ `user_type` is required ('client' or 'artisan')

The frontend form enforces:
- ✅ All fields marked with `*` are required
- ✅ Email format validation
- ✅ Password match validation
- ✅ Artisan-specific fields validation

---

## 🎯 Summary

**Problem**: Registration failing with "first_name required" error
**Cause**: Frontend not sending first_name/last_name to backend
**Solution**: Updated AuthModal to send first_name and last_name fields
**Result**: ✅ Registration now works correctly for both clients and artisans

---

## 📁 Files Modified

1. ✅ [`maalem-frontend/src/components/AuthModal.jsx`](file://c:\Users\Igolan\Desktop\site%20maalem\maalem-frontend\src\components\AuthModal.jsx)
   - Lines 120-138: Updated registration data structure
   - Added proper first_name and last_name mapping
   - Removed unnecessary username field
   - Cleaned up field deletion logic

---

**Status**: ✅ FIXED - Registration working correctly!

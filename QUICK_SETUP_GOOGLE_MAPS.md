# Quick Setup Guide - Google Maps Integration

## 🚀 Quick Start (5 minutes)

### Step 1: Get Your Google Maps API Key

1. Go to: https://console.cloud.google.com/google/maps-apis
2. Click **"Create Project"** or select existing project
3. Click **"Enable APIs and Services"**
4. Search for **"Maps JavaScript API"** and enable it
5. Go to **"Credentials"** tab
6. Click **"Create Credentials"** → **"API Key"**
7. **Copy your API key** (starts with `AIza...`)

### Step 2: Configure Your Project

Open `maalem-frontend/.env` and replace the placeholder:

```env
VITE_GOOGLE_MAPS_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Step 3: Restart Your Dev Server

```bash
# Press Ctrl+C to stop the server
# Then restart:
npm run dev
```

### Step 4: Test It!

1. Navigate to **Maalems** page
2. Click the **"Localisation"** button
3. See the map with artisan markers! 🗺️

---

## ✨ Features You Get

### 1. Your Profile Hidden from List
- ✅ You won't see your own profile in the Maalems list
- ✅ Only other artisans are shown

### 2. Interactive Google Maps
- 🗺️ Full interactive map with zoom, pan, street view
- 📍 Custom blue markers for each artisan
- 🧭 Your location shown as blue circle (if you allow)
- 🎯 Click markers to see artisan details
- 📱 Quick actions: View profile or WhatsApp

### 3. Smart Features
- **Auto-zoom**: Map automatically fits to show all artisans
- **Info cards**: Click any marker to see details
- **"Ma position" button**: Center map on your location
- **Count display**: Shows how many artisans have location data

---

## 🔧 Secure Your API Key (Important!)

### In Google Cloud Console:

1. **Application Restrictions**:
   - Set HTTP referrers: `http://localhost:*`, `https://yourdomain.com/*`
   
2. **API Restrictions**:
   - Select: "Restrict key"
   - Choose: "Maps JavaScript API"

3. **Set Usage Limits**:
   - Daily limit: 1000 requests (adjust as needed)
   - This prevents unexpected charges

---

## 📊 Free Tier Limits

Google Maps offers generous free tier:
- **$200/month free credit**
- ≈ **28,000 map loads per month free**
- Perfect for small to medium apps!

---

## ⚠️ Troubleshooting

### Map doesn't show?
1. Check if API key is set in `.env`
2. Restart dev server after changing `.env`
3. Check browser console for errors
4. Verify Maps JavaScript API is enabled in Google Cloud

### Markers don't appear?
1. Artisans need latitude/longitude in database
2. Check backend is sending `latitude` and `longitude` fields
3. Open browser console to see if coordinates are present

### "Votre position" doesn't work?
1. Allow location permission in browser
2. Check if you're using HTTPS (required for geolocation)
3. Localhost works without HTTPS

---

## 🎓 For Developers

### Adding Location to Artisans

In Django admin or shell:
```python
from users.models import User

# Casablanca coordinates
artisan = User.objects.get(id=1)
artisan.latitude = 33.5731
artisan.longitude = -7.5898
artisan.save()
```

### Test Coordinates (Morocco Cities)

```python
# Casablanca
latitude = 33.5731, longitude = -7.5898

# Rabat
latitude = 34.0209, longitude = -6.8416

# Marrakech
latitude = 31.6295, longitude = -7.9811

# Fes
latitude = 34.0181, longitude = -5.0078

# Tangier
latitude = 35.7595, longitude = -5.8340
```

---

## 📝 What Changed in Code

### New Files:
- ✅ `src/components/ArtisanMap.jsx` - Google Maps component

### Modified Files:
- ✅ `src/pages/Maalems.jsx` - Integrated map component
- ✅ `src/services/artisans.js` - Filter current user + add lat/lng
- ✅ `.env` - Added Google Maps API key
- ✅ `.env.example` - Updated example config

---

## 🎉 You're All Set!

Your Maalem platform now has:
- ✅ Professional Google Maps integration
- ✅ Hidden self-profile from artisan list
- ✅ Location-based artisan discovery
- ✅ Interactive map with custom markers
- ✅ Mobile-friendly responsive design

Enjoy! 🚀

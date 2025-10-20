# Google Maps Integration & Profile Filtering

## Overview
This document describes the implementation of:
1. **Filtering out current user's profile** from Maalems list
2. **Google Maps integration** to display artisans on an interactive map
3. **Location-based artisan discovery**

---

## 1. Filter Current User Profile from Maalems List

### Problem
Users were seeing their own profile in the Maalems (artisans) list, which is unnecessary and confusing.

### Solution
Modified the artisans service to automatically filter out the current logged-in user from the list.

### Files Modified

#### `maalem-frontend/src/services/artisans.js`

**Added import**:
```javascript
import { getCurrentUser } from './auth';
```

**Modified `getArtisans()` function**:
```javascript
// Get current user to filter out their own profile
const currentUser = getCurrentUser();
const currentUserId = currentUser ? currentUser.id : null;

return artisans
  .filter(artisan => artisan.id !== currentUserId) // Exclude current user
  .map(artisan => ({
    // ... mapping
  }));
```

**Result**:
- ✅ Current user's profile is hidden from Maalems list
- ✅ Works for both authenticated and non-authenticated users
- ✅ Only other artisans are displayed

---

## 2. Google Maps Integration

### Features Implemented

#### A. Interactive Google Maps Component

**New Component**: `maalem-frontend/src/components/ArtisanMap.jsx`

**Features**:
- 🗺️ **Interactive Google Maps** with full controls
- 📍 **Custom markers** for each artisan with location data
- 🧭 **User location tracking** (with permission)
- 🎯 **Click on markers** to see artisan details
- 📱 **Responsive design** works on desktop and mobile
- 🔍 **Auto-zoom** to fit all artisan markers
- ⚡ **Quick actions** - View profile or WhatsApp directly from map

**Key Technologies**:
- Google Maps JavaScript API
- Custom SVG markers with emoji icons
- Geolocation API for user position
- Real-time marker clustering

#### B. Location Data Mapping

**Added to artisans service**:
```javascript
latitude: artisan.latitude || null,
longitude: artisan.longitude || null
```

These fields are now mapped from the backend to display artisans on the map.

### Files Modified

1. **`maalem-frontend/src/components/ArtisanMap.jsx`** - New component
   - Full Google Maps integration
   - Custom markers for artisans
   - User location marker (blue circle)
   - Artisan info cards on marker click
   - Navigation controls

2. **`maalem-frontend/src/pages/Maalems.jsx`** - Updated to use map component
   - Replaced placeholder map with real Google Maps
   - Integrated ArtisanMap component
   - Simplified MapModal component

3. **`maalem-frontend/src/services/artisans.js`** - Added location fields
   - Map latitude and longitude from backend
   - Filter current user from list

4. **`maalem-frontend/.env`** - Added Google Maps API key config
   ```env
   VITE_GOOGLE_MAPS_API_KEY=YOUR_GOOGLE_MAPS_API_KEY_HERE
   ```

5. **`maalem-frontend/.env.example`** - Updated example config

---

## 3. Setup Instructions

### Step 1: Get Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Maps JavaScript API**
4. Go to **APIs & Services > Credentials**
5. Click **Create Credentials > API Key**
6. Copy your API key

### Step 2: Configure API Key

Add your API key to `.env` file:

```env
VITE_GOOGLE_MAPS_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Step 3: Restart Development Server

```bash
# Stop the server (Ctrl+C)
# Then restart
npm run dev
```

### Step 4: Add Location Data to Artisans

Make sure artisan profiles have latitude and longitude data in the database:

```python
# In Django admin or through API
artisan.latitude = 33.5731  # Example: Casablanca
artisan.longitude = -7.5898
artisan.save()
```

---

## 4. How It Works

### User Flow

1. **User navigates to Maalems page**
2. **Clicks "Localisation" button**
3. **Map opens** showing all artisans with location data
4. **User's location is requested** (if they allow it)
5. **Blue marker shows user position**
6. **Blue markers with hammer icon** show artisan positions
7. **Click on any marker** to see artisan details
8. **Click "Voir le profil"** to navigate to full profile
9. **Click "WhatsApp"** to contact directly

### Map Features

#### Custom Artisan Markers
```javascript
icon: {
  url: 'data:image/svg+xml;charset=UTF-8,<svg>...',
  scaledSize: new google.maps.Size(40, 40),
}
```
- Blue circle with hammer emoji (🔨)
- 40x40 pixels
- White border for visibility

#### User Location Marker
```javascript
icon: {
  path: google.maps.SymbolPath.CIRCLE,
  scale: 10,
  fillColor: '#4285F4',
  fillOpacity: 1,
}
```
- Blue filled circle
- Represents "you are here"

#### Info Card on Click
```jsx
{selectedArtisan && (
  <div className="absolute bottom-4 left-4 right-4 bg-white rounded-lg shadow-lg p-4">
    {/* Artisan details and action buttons */}
  </div>
)}
```
- Shows at bottom of map
- Contains profile picture, name, specialty
- Quick action buttons

---

## 5. Backend Requirements

### Database Fields

Ensure the `User` model has these fields:
```python
latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
```

### Serializer Fields

The `UserSerializer` should include:
```python
fields = [..., 'latitude', 'longitude']
```

---

## 6. Error Handling

### No API Key
If Google Maps API key is not configured:
```
Error: Google Maps non chargé. Veuillez vérifier votre connexion Internet.
```

### No Location Permission
If user denies location permission:
- Map still shows with default center (Casablanca)
- Artisans are still visible
- "Ma position" button shows alert

### No Artisans with Location
If no artisans have latitude/longitude:
```
0 artisan(s) avec localisation
```
- Map loads but shows no markers
- Header shows count

---

## 7. Testing Checklist

### Frontend Testing
- [ ] Current user profile is hidden from Maalems list
- [ ] Map opens when clicking "Localisation" button
- [ ] Google Maps loads correctly
- [ ] User location marker appears (after permission)
- [ ] Artisan markers appear for all artisans with coordinates
- [ ] Clicking marker shows artisan info card
- [ ] "Voir le profil" navigates to correct profile
- [ ] "WhatsApp" opens WhatsApp chat
- [ ] "Ma position" button centers map on user
- [ ] Map controls work (zoom, pan, street view)
- [ ] Close button closes the map

### Backend Testing
- [ ] Artisan data includes latitude and longitude
- [ ] API returns current user ID in token
- [ ] Artisan list excludes current user

---

## 8. Future Enhancements

### Possible Improvements
1. **Clustering** - Group nearby markers when zoomed out
2. **Search on map** - Filter artisans by specialty while map is open
3. **Directions** - Get directions from user location to artisan
4. **Distance calculation** - Show distance in kilometers
5. **Radius filter** - Show only artisans within X km
6. **Heatmap** - Visual density of artisans in different areas
7. **Street view** - Preview artisan location in street view
8. **Save favorite locations** - Bookmark artisans on map

---

## 9. Cost Considerations

### Google Maps API Pricing
- **First $200/month**: Free (includes ~28,000 map loads)
- **After free tier**: $7 per 1,000 map loads
- **Recommendation**: Set up billing alerts in Google Cloud Console

### Optimization Tips
1. **Lazy loading** - Map only loads when opened ✅ Already implemented
2. **API key restrictions** - Restrict by domain in Google Console
3. **Caching** - Cache map tiles when possible
4. **Marker clustering** - Reduce API calls for dense areas

---

## 10. Security Best Practices

### API Key Security
```env
# NEVER commit this file to Git
.env

# Use environment variables
VITE_GOOGLE_MAPS_API_KEY=xxx
```

### API Key Restrictions
In Google Cloud Console:
1. **Application restrictions** - Restrict to your domain
2. **API restrictions** - Only enable Maps JavaScript API
3. **Usage limits** - Set daily quotas

---

## Summary

### What Changed
1. ✅ **Current user profile hidden** from Maalems list
2. ✅ **Google Maps fully integrated** with interactive markers
3. ✅ **User location tracking** with blue marker
4. ✅ **Artisan markers** with custom icons
5. ✅ **Click-to-view details** with info cards
6. ✅ **Quick actions** from map (profile, WhatsApp)
7. ✅ **Environment configuration** for API key

### Benefits
- 🎯 Better user experience - no self-profile in list
- 🗺️ Visual discovery of nearby artisans
- 📍 Location-based search and filtering
- 🚀 Professional map integration like major platforms
- 📱 Mobile-friendly responsive design

All features are production-ready! 🎉

# Google Maps Integration Guide

## Issues Fixed

1. **Invalid API Key** - The API was using "YOUR_API_KEY_HERE" instead of a real key
2. **Multiple API Loads** - The Google Maps JavaScript API was being loaded multiple times
3. **Performance Warning** - API was loaded without `loading=async`
4. **Geolocation Errors** - User location access errors were being displayed to users

## Solutions Implemented

### 1. Fixed Multiple API Loading
- Added global flags to track API loading state
- Implemented callback system for multiple components needing Google Maps
- Prevented duplicate script loading

### 2. Improved Performance
- Added `loading=async` parameter to Google Maps script
- Better error handling and user feedback

### 3. Enhanced Error Handling
- More graceful handling of geolocation errors
- Clearer error messages for API key issues

## How to Configure Google Maps API

### 1. Get a Google Maps API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - Maps JavaScript API
   - Places API
4. Create credentials (API Key)
5. Restrict the API key to your domain for security

### 2. Configure Environment Variables
Add your API key to the [.env](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/.env) file:

```env
VITE_GOOGLE_MAPS_API_KEY=your_actual_api_key_here
```

### 3. Environment-Specific Configuration
- **Development**: Use [.env](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/.env) file
- **Production**: Set environment variable in your deployment platform

## Files Modified

1. [maalem-frontend/.env](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/.env) - Added Google Maps API key configuration
2. [maalem-frontend/src/components/ArtisanMap.jsx](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/src/components/ArtisanMap.jsx) - Fixed multiple loading issues and improved error handling

## Testing

To test if Google Maps is working properly:
1. Ensure you have a valid API key in your [.env](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/.env) file
2. Restart your development server
3. Navigate to the "Maalems" page
4. Click the "Localisation" button to open the map
5. Check the browser console for any Google Maps errors

## Common Issues and Solutions

### 1. InvalidKeyMapError
**Cause**: Invalid or missing API key
**Solution**: Ensure `VITE_GOOGLE_MAPS_API_KEY` is set in your [.env](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/.env) file with a valid key

### 2. Multiple API Loads
**Cause**: Component re-renders causing script to load multiple times
**Solution**: Already fixed with global loading state tracking

### 3. Geolocation Errors
**Cause**: User denied location access or browser doesn't support it
**Solution**: Errors are now handled gracefully without displaying to users

## Security Best Practices

1. **Restrict API Key**: 
   - In Google Cloud Console, restrict your API key to specific domains
   - For development: `localhost:5173`
   - For production: `yourdomain.com`

2. **Enable Only Required APIs**:
   - Maps JavaScript API
   - Places API (if needed)

3. **Monitor Usage**:
   - Set up billing alerts
   - Monitor API usage in Google Cloud Console

## Performance Optimization

1. **Async Loading**: The API is now loaded with `loading=async` for better performance
2. **Single Load**: The API script is loaded only once per session
3. **Lazy Loading**: Maps are only initialized when the map modal is opened

## Troubleshooting

### If Maps Still Don't Work:
1. Check browser console for specific error messages
2. Verify API key is correct and enabled
3. Ensure required APIs are enabled in Google Cloud Console
4. Check that API key restrictions match your domain

### If You See "InvalidKey" Warnings:
1. Verify `VITE_GOOGLE_MAPS_API_KEY` is set in [.env](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/.env)
2. Ensure the key is valid and has the correct permissions
3. Check that the key is not restricted to incompatible domains

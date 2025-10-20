# Improved Localisation Features

## Features Implemented

1. **5km Radius Filtering** - Only show artisans within 5 kilometers of the user's location
2. **Distance Calculation** - Accurate distance calculation using the haversine formula
3. **Distance Display** - Show distance to each artisan in the map markers and info cards
4. **Better Error Handling** - Improved handling of geolocation and API errors
5. **Performance Optimizations** - Prevented multiple Google Maps API loads

## Technical Details

### Distance Calculation
Implemented the haversine formula for accurate distance calculation between two points on Earth:

```javascript
const calculateDistance = (lat1, lon1, lat2, lon2) => {
  const R = 6371; // Earth radius in kilometers
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
    Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  const d = R * c;
  return d;
};
```

### 5km Radius Filtering
Artisans are automatically filtered to show only those within a 5km radius of the user's location:

```javascript
const filteredArtisans = filterArtisansByRadius(
  artisans, 
  userLocation.lat, 
  userLocation.lng, 
  5 // 5km radius
);
```

### Distance Display
Distances are formatted for better readability:
- Less than 1km: Display in meters (e.g., "450 m")
- 1km or more: Display in kilometers (e.g., "2.3 km")

## Files Modified

1. [maalem-frontend/src/utils/distanceUtils.js](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/src/utils/distanceUtils.js) - New utility functions for distance calculation
2. [maalem-frontend/src/components/ArtisanMap.jsx](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/src/components/ArtisanMap.jsx) - Updated map component with 5km filtering and distance display
3. [maalem-frontend/.env](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/.env) - Updated environment configuration

## How to Use

### 1. Configure Google Maps API Key
To use the improved localisation features, you need a valid Google Maps API key:

1. Get a Google Maps API Key from [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the following APIs:
   - Maps JavaScript API
   - Places API
3. Add your API key to the [.env](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/.env) file:
   ```env
   VITE_GOOGLE_MAPS_API_KEY=your_actual_api_key_here
   ```

### 2. Test the Features
1. Restart your development server
2. Navigate to the "Maalems" page
3. Click the "Localisation" button
4. Grant location permission when prompted
5. The map will show only artisans within 5km of your location
6. Each artisan marker will display the distance
7. Clicking on an artisan will show the distance in the info card

## Benefits

1. **More Relevant Results** - Users see only nearby artisans
2. **Better User Experience** - Clear distance information helps users make decisions
3. **Improved Performance** - Fewer markers on the map means better performance
4. **Accurate Calculations** - Haversine formula provides accurate distance measurements
5. **Responsive Design** - Distance display adapts to different ranges

## Troubleshooting

### If Artisans Don't Appear
1. Check that artisans have latitude and longitude coordinates in the database
2. Verify that the user's location is being detected
3. Ensure the Google Maps API key is valid and properly configured

### If Distance Shows as "undefined"
1. Make sure the artisan objects have valid latitude and longitude values
2. Check that the user's location is available

### If Map Doesn't Load
1. Verify the Google Maps API key is correct
2. Check browser console for specific error messages
3. Ensure required APIs are enabled in Google Cloud Console

## Future Improvements

1. **Configurable Radius** - Allow users to adjust the radius (1km, 5km, 10km, etc.)
2. **Sort by Distance** - Show nearest artisans first
3. **Save Favorite Locations** - Allow users to bookmark locations
4. **Direction Integration** - Provide directions to artisans
5. **Advanced Filtering** - Filter by specialty within radius
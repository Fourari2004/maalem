# API Connection Fix Summary

## Problem Identified
The React frontend was unable to connect to the Django backend API, showing `net::ERR_CONNECTION_TIMED_OUT` errors when trying to access endpoints like:
- `192.168.68.58:8000/api/posts/`

## Root Causes
1. **Incorrect API URL Configuration**: The frontend [.env](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/.env) file was configured to use a specific IP address (`192.168.68.58`) which wasn't accessible
2. **Backend Server Not Running**: The Django backend server was not running or had stopped

## Solutions Implemented

### 1. Fixed Frontend Configuration
Updated [maalem-frontend/.env](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/.env) to use localhost instead of the specific IP:
```env
# Configuration locale (décommentez celle-ci pour le développement local)
VITE_API_URL=http://localhost:8000/api
```

### 2. Started Backend Server
Launched both servers using the PowerShell script:
```bash
powershell -ExecutionPolicy Bypass -File "start_servers.ps1"
```

### 3. Verified Connection
Confirmed both services are accessible:
- Frontend: http://localhost:5173 (Status: 200)
- Backend API: http://localhost:8000/api/posts/ (Status: 200)

## Configuration Details

### Frontend (.env)
```env
# Configuration locale (décommentez celle-ci pour le développement local)
VITE_API_URL=http://localhost:8000/api
```

### Services Configuration
All frontend services ([posts.js](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/src/services/posts.js), [artisans.js](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/src/services/artisans.js), [auth.js](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/src/services/auth.js)) use the same pattern:
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
```

## Testing Verification
✅ HTTP Status 200 for both frontend and backend API endpoints
✅ Posts can be fetched successfully from the frontend
✅ All API endpoints are accessible

## For Mobile Access
To access from mobile devices on the same network:
1. Uncomment the mobile configuration in [.env](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/.env):
   ```env
   VITE_API_URL=http://YOUR_COMPUTER_IP:8000/api
   ```
2. Replace `YOUR_COMPUTER_IP` with your computer's actual IP address on the local network
3. Ensure Windows Firewall allows connections on port 8000

## Prevention
To prevent this issue in the future:
1. Always ensure both backend and frontend servers are running
2. Use the provided startup scripts ([start_servers.ps1](file:///C:/Users/Igolan/Desktop/site%20maalem/start_servers.ps1) or [start_servers.bat](file:///C:/Users/Igolan/Desktop/site%20maalem/start_servers.bat))
3. Keep both terminal windows open (one for backend, one for frontend)
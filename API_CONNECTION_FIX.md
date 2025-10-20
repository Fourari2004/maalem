# API Connection Fix Summary

## Problem
The React frontend was unable to connect to the Django backend API, showing `net::ERR_CONNECTION_TIMED_OUT` errors when trying to access endpoints like:
- `192.168.68.58:8000/api/posts/`
- `192.168.68.58:8000/api/users/artisans/`
- `192.168.68.58:8000/api/users/login/client/`

## Root Causes
1. **Incorrect API URL Configuration**: The frontend [.env](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/.env) file was configured to use a specific IP address (`192.168.68.58`) which might not be accessible
2. **Backend Server Not Running**: The backend Django server was not running or not accessible on the specified IP
3. **Network/Firewall Issues**: Possible network or firewall restrictions preventing connection to the specified IP

## Solutions Implemented

### 1. Updated Frontend Configuration
Modified [maalem-frontend/.env](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/.env) to use localhost instead of the specific IP:
```env
# Configuration locale (décommentez celle-ci pour le développement local)
VITE_API_URL=http://localhost:8000/api
```

### 2. Started Backend Server
Launched the Django backend server using the PowerShell script:
```bash
powershell -ExecutionPolicy Bypass -File "start_servers.ps1"
```

### 3. Verified Connection
Confirmed the backend is accessible:
- Backend running on: `http://localhost:8000`
- API endpoint accessible: `http://localhost:8000/api/posts/`
- Status code: 200 (OK)

## Configuration Details

### Frontend (.env)
```env
# Configuration locale (décommentez celle-ci pour le développement local)
VITE_API_URL=http://localhost:8000/api
```

### Backend (settings.py)
CORS is properly configured to allow localhost connections:
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000', 
    'http://localhost:5173',
    'http://localhost:5185',
    'http://192.168.68.58:5173',
    'http://192.168.68.58:5185'
]
```

### Services Configuration
All frontend services ([posts.js](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/src/services/posts.js), [artisans.js](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/src/services/artisans.js), [auth.js](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/src/services/auth.js)) use the same pattern:
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
```

## Testing
Created a test component to verify the connection is working properly.

## For Mobile Access
To access from mobile devices on the same network:
1. Uncomment the mobile configuration in [.env](file:///C:/Users/Igolan/Desktop/site%20maalem/maalem-frontend/.env):
   ```env
   VITE_API_URL=http://YOUR_COMPUTER_IP:8000/api
   ```
2. Replace `YOUR_COMPUTER_IP` with your computer's actual IP address on the local network
3. Ensure Windows Firewall allows connections on port 8000

## Verification Commands
```bash
# Test if backend is running
curl -I http://localhost:8000/api/posts/

# Or using Python
python -c "import requests; print(requests.head('http://localhost:8000/api/posts/').status_code)"
```
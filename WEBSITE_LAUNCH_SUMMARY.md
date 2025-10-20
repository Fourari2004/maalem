# Website Launch Summary

## Servers Started Successfully

### Backend Server (Django)
- **URL**: http://localhost:8000
- **API Endpoint**: http://localhost:8000/api/
- **Status**: ✅ Running

### Frontend Server (React/Vite)
- **URL**: http://localhost:5173
- **Status**: ✅ Running

## Verification Results
- ✅ Frontend accessible at http://localhost:5173 (Status: 200)
- ✅ Backend API accessible at http://localhost:8000/api/posts/ (Status: 200)

## How to Access the Website
1. Open your web browser
2. Navigate to http://localhost:5173

## Network Access
The website is also accessible from other devices on the same network:
- http://172.24.240.1:5173
- http://10.36.49.242:5173
- http://192.168.137.22:5173

## Important Notes
1. Keep both terminal windows open:
   - One running the Django backend server
   - One running the React frontend development server
2. If you close either terminal, the corresponding service will stop
3. To stop the servers, simply close both terminal windows

## Troubleshooting
If you encounter issues:
1. Check that both terminals remain open
2. Verify the .env file in maalem-frontend has VITE_API_URL=http://localhost:8000/api
3. Make sure no firewall is blocking the connections
4. Restart both servers using the start_servers.ps1 script if needed

## Commands Used
```powershell
# Start both servers
powershell -ExecutionPolicy Bypass -File "start_servers.ps1"

# Or start servers individually
cd maalem-backend && python manage.py runserver
cd maalem-frontend && npm run dev
```
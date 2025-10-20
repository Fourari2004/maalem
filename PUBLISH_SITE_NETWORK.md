# Publishing Your Site on the Network

## Available Solutions

### 1. One-Click Launch (Recommended) ⚡
The easiest way to publish your site on the network is using the one-click launch script.

**Steps:**
1. Double-click on `LANCER_TOUT.ps1` (PowerShell script)
2. If Windows blocks it, right-click → "Run with PowerShell"
3. Follow the on-screen instructions
4. Your site will be accessible at `http://YOUR_IP:5173`

**Features:**
- ✅ Automatic IP detection
- ✅ Automatic configuration for mobile access
- ✅ Backend and frontend launch
- ✅ Firewall configuration
- ✅ Dependency verification

### 2. Public Access Script 🌐
For immediate network access:

**Steps:**
1. Double-click on `start_public.ps1`
2. If Windows blocks it, right-click → "Run with PowerShell"
3. The script will:
   - Detect your local IP address
   - Configure backend to accept connections
   - Configure frontend with correct API URL
   - Launch both servers
4. Access from any device on the same WiFi at `http://YOUR_IP:5173`

### 3. Manual Configuration 🔧
If you prefer to do it manually:

**Steps:**
1. Find your IP address:
   ```powershell
   ipconfig
   # Look for "IPv4 Address" (e.g., 192.168.1.100)
   ```

2. Update backend configuration in `maalem-backend/.env`:
   ```env
   ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,YOUR_IP_ADDRESS
   CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://YOUR_IP_ADDRESS:5173
   ```

3. Update frontend configuration in `maalem-frontend/.env`:
   ```env
   VITE_API_URL=http://YOUR_IP_ADDRESS:8000/api
   ```

4. Start backend:
   ```powershell
   cd "c:\Users\Igolan\Desktop\site maalem\maalem-backend"
   python manage.py runserver 0.0.0.0:8000
   ```

5. Start frontend in a new terminal:
   ```powershell
   cd "c:\Users\Igolan\Desktop\site maalem\maalem-frontend"
   npm run dev -- --host 0.0.0.0
   ```

6. Access from any device on the same network:
   `http://YOUR_IP_ADDRESS:5173`

## Firewall Configuration

If other devices can't access your site:

1. **Run the firewall configuration script:**
   - Double-click `configure_firewall.ps1` as Administrator
   - This will automatically configure Windows Firewall

2. **Or configure manually:**
   - Open Windows Defender Firewall with Advanced Security
   - Click "Inbound Rules" → "New Rule"
   - Select "Port" → Next
   - Select "TCP" and specify ports "8000,5173" → Next
   - Select "Allow the connection" → Next
   - Check all profiles → Next
   - Name the rule "Maalem Development" → Finish

## Access Instructions

### From Your Computer:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000

### From Other Devices (Phone, Tablet, etc.):
1. Make sure all devices are on the same WiFi network
2. Open browser on the other device
3. Go to: `http://YOUR_COMPUTER_IP:5173`
   (Replace YOUR_COMPUTER_IP with your actual IP address)

## Troubleshooting

### Site Not Loading on Other Devices:
1. Check that both servers are running
2. Verify firewall settings
3. Ensure IP address is correct in configurations
4. Make sure all devices are on the same network

### CORS Errors:
1. Check `CORS_ALLOWED_ORIGINS` in backend .env
2. Restart backend server after configuration changes

### Connection Refused:
1. Make sure backend is running on `0.0.0.0:8000`
2. Check that frontend is running with `--host` flag

## Security Notes

⚠️ **Important:** These configurations are for development purposes only.
- Do not use in production environments
- The site will be accessible to anyone on your network
- Make sure to stop the servers when not in use

## Recommended Approach

For the easiest experience, use the one-click launch:
1. Double-click `LANCER_TOUT.ps1`
2. Follow the prompts
3. Access your site from any device on the same network

This will automatically handle all configuration and launch both servers with proper network access.
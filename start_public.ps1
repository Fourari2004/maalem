# Script pour démarrer le site Maalem en mode réseau local
# Accessible depuis n'importe quel appareil sur le même réseau WiFi

Write-Host "🚀 Démarrage du site Maalem en mode réseau local..." -ForegroundColor Cyan
Write-Host ""

# Obtenir l'adresse IP locale
$ipAddress = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi*" | Select-Object -First 1).IPAddress

if (-not $ipAddress) {
    $ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*"} | Select-Object -First 1).IPAddress
}

Write-Host "📍 Votre adresse IP locale: $ipAddress" -ForegroundColor Green
Write-Host ""

# Mettre à jour les configurations
Write-Host "⚙️  Configuration du backend..." -ForegroundColor Yellow

$backendEnv = "DEBUG=True
SECRET_KEY=Ft15082004
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,$ipAddress
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://${ipAddress}:5173

# Database
DB_NAME=maalem_db
DB_USER=postgres
DB_PASSWORD=Ft15082004
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=fourari2004@gmail.com
EMAIL_HOST_PASSWORD=Ft15082004

# AWS S3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=your-region"

Set-Content -Path "maalem-backend\.env" -Value $backendEnv

Write-Host "⚙️  Configuration du frontend..." -ForegroundColor Yellow
$frontendEnv = "VITE_API_URL=http://${ipAddress}:8000/api"
Set-Content -Path "maalem-frontend\.env" -Value $frontendEnv

Write-Host ""
Write-Host "✅ Configuration terminée!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Le site sera accessible à:" -ForegroundColor Cyan
Write-Host "   http://$ipAddress:5173" -ForegroundColor White
Write-Host ""
Write-Host "📱 Scannez ce QR code depuis votre téléphone (généré sur https://www.qr-code-generator.com/):" -ForegroundColor Cyan
Write-Host "   URL: http://$ipAddress:5173" -ForegroundColor White
Write-Host ""

# Démarrer le backend
Write-Host "🔧 Démarrage du backend Django..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'c:\Users\Igolan\Desktop\site maalem\maalem-backend'; python manage.py runserver 0.0.0.0:8000"

Start-Sleep -Seconds 3

# Démarrer le frontend
Write-Host "🎨 Démarrage du frontend React..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'c:\Users\Igolan\Desktop\site maalem\maalem-frontend'; npm run dev -- --host 0.0.0.0"

Write-Host ""
Write-Host "✨ Les serveurs démarrent..." -ForegroundColor Green
Write-Host ""
Write-Host "📋 Instructions:" -ForegroundColor Cyan
Write-Host "   1. Attendez quelques secondes que les serveurs démarrent" -ForegroundColor White
Write-Host "   2. Ouvrez un navigateur sur n'importe quel appareil du même réseau WiFi" -ForegroundColor White
Write-Host "   3. Tapez: http://$ipAddress:5173" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  Assurez-vous que:" -ForegroundColor Yellow
Write-Host "   - Votre pare-feu Windows autorise les connexions sur les ports 8000 et 5173" -ForegroundColor White
Write-Host "   - Tous les appareils sont sur le même réseau WiFi" -ForegroundColor White
Write-Host ""
Write-Host "🛑 Pour arrêter les serveurs, fermez les fenêtres PowerShell qui se sont ouvertes" -ForegroundColor Red
Write-Host ""
Write-Host "Appuyez sur une touche pour continuer..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

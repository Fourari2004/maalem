# Script pour lancer le frontend avec accès mobile
# Ce script configure le serveur pour être accessible depuis votre téléphone

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  LANCEMENT DU SITE POUR ACCÈS MOBILE  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Obtenir l'adresse IP locale
$localIP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias Wi-Fi).IPAddress
Write-Host "Adresse IP de votre ordinateur: $localIP" -ForegroundColor Green
Write-Host ""

# Copier le fichier de configuration mobile
Copy-Item -Path ".env.mobile" -Destination ".env" -Force
Write-Host "✓ Configuration mobile activée (.env.mobile -> .env)" -ForegroundColor Green
Write-Host ""

Write-Host "Lancement du serveur frontend..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ACCÈS AU SITE :" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Depuis cet ordinateur: http://localhost:5173" -ForegroundColor White
Write-Host "Depuis votre téléphone: http://${localIP}:5173" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANT: Assurez-vous que:" -ForegroundColor Yellow
Write-Host "  1. Le backend Django est lancé (python manage.py runserver 0.0.0.0:8000)" -ForegroundColor White
Write-Host "  2. Votre téléphone est sur le MÊME réseau WiFi" -ForegroundColor White
Write-Host "  3. Le pare-feu Windows autorise les ports 5173 et 8000" -ForegroundColor White
Write-Host ""
Write-Host "Appuyez sur Ctrl+C pour arrêter le serveur" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Lancer le serveur avec l'option --host pour accepter les connexions externes
npm run dev -- --host

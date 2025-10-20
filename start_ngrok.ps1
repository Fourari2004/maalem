# Script PowerShell pour lancer le site avec accès Internet global (ngrok)

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  LANCEMENT DU SITE AVEC ACCÈS INTERNET GLOBAL (ngrok)" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANT: Vous devez avoir installé ngrok avant d'utiliser ce script" -ForegroundColor Yellow
Write-Host "Si ce n'est pas fait, visitez: https://ngrok.com/download" -ForegroundColor Yellow
Write-Host ""
Write-Host "Ce script va lancer 4 terminaux:" -ForegroundColor White
Write-Host "  1. Backend Django (port 8000)" -ForegroundColor White
Write-Host "  2. Frontend Vite (port 5173)" -ForegroundColor White
Write-Host "  3. Tunnel ngrok Backend" -ForegroundColor White
Write-Host "  4. Tunnel ngrok Frontend" -ForegroundColor White
Write-Host ""
Write-Host "Appuyez sur une touche pour continuer..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Vérifier si ngrok est installé
if (-not (Get-Command ngrok -ErrorAction SilentlyContinue)) {
    Write-Host ""
    Write-Host "ERREUR: ngrok n'est pas installé ou n'est pas dans le PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Pour installer ngrok:" -ForegroundColor Yellow
    Write-Host "1. Téléchargez depuis: https://ngrok.com/download" -ForegroundColor White
    Write-Host "2. Extrayez ngrok.exe dans un dossier (ex: C:\ngrok\)" -ForegroundColor White
    Write-Host "3. Ajoutez ce dossier au PATH système ou utilisez le chemin complet" -ForegroundColor White
    Write-Host ""
    pause
    exit
}

# Lancer le backend Django
Write-Host "Lancement du backend Django..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\maalem-backend'; python manage.py runserver 0.0.0.0:8000"
Start-Sleep -Seconds 5

# Lancer le frontend Vite
Write-Host "Lancement du frontend Vite..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\maalem-frontend'; npm run dev -- --host"
Start-Sleep -Seconds 10

# Lancer ngrok pour le backend
Write-Host "Lancement du tunnel ngrok pour le backend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "ngrok http 8000"
Start-Sleep -Seconds 3

# Lancer ngrok pour le frontend
Write-Host "Lancement du tunnel ngrok pour le frontend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "ngrok http 5173"

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "SERVEURS LANCÉS!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "PROCHAINES ÉTAPES:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Dans la fenêtre 'ngrok Backend', notez l'URL (ex: https://xxxx.ngrok-free.app)" -ForegroundColor White
Write-Host "2. Dans la fenêtre 'ngrok Frontend', notez l'URL (ex: https://yyyy.ngrok-free.app)" -ForegroundColor White
Write-Host ""
Write-Host "3. Mettez à jour le fichier: maalem-backend\config\settings.py" -ForegroundColor White
Write-Host "   - Ajoutez l'URL ngrok backend dans ALLOWED_HOSTS" -ForegroundColor Gray
Write-Host "   - Ajoutez l'URL ngrok frontend dans CORS_ALLOWED_ORIGINS" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Créez le fichier: maalem-frontend\.env.ngrok avec:" -ForegroundColor White
Write-Host "   VITE_API_URL=https://xxxx-backend.ngrok-free.app/api" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Copiez la config:" -ForegroundColor White
Write-Host "   cd maalem-frontend" -ForegroundColor Gray
Write-Host "   copy .env.ngrok .env" -ForegroundColor Gray
Write-Host ""
Write-Host "6. Redémarrez le frontend" -ForegroundColor White
Write-Host ""
Write-Host "7. Partagez l'URL frontend ngrok avec qui vous voulez!" -ForegroundColor Green
Write-Host ""
Write-Host "Voir ACCES_INTERNET_GLOBAL.md pour plus de détails" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

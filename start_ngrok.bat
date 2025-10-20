@echo off
echo ================================================================
echo   LANCEMENT DU SITE AVEC ACCES INTERNET GLOBAL (ngrok)
echo ================================================================
echo.
echo IMPORTANT: Vous devez avoir installe ngrok avant d'utiliser ce script
echo Si ce n'est pas fait, visitez: https://ngrok.com/download
echo.
echo Ce script va lancer 4 terminaux:
echo   1. Backend Django (port 8000)
echo   2. Frontend Vite (port 5173)
echo   3. Tunnel ngrok Backend
echo   4. Tunnel ngrok Frontend
echo.
pause

REM Lancer le backend Django
start "Backend Django" cmd /k "cd maalem-backend && python manage.py runserver 0.0.0.0:8000"
timeout /t 5

REM Lancer le frontend Vite
start "Frontend Vite" cmd /k "cd maalem-frontend && npm run dev -- --host"
timeout /t 10

REM Lancer ngrok pour le backend
start "ngrok Backend" cmd /k "ngrok http 8000"
timeout /t 3

REM Lancer ngrok pour le frontend
start "ngrok Frontend" cmd /k "ngrok http 5173"

echo.
echo ================================================================
echo SERVEURS LANCES!
echo ================================================================
echo.
echo PROCHAINES ETAPES:
echo.
echo 1. Dans la fenetre "ngrok Backend", notez l'URL (ex: https://xxxx.ngrok-free.app)
echo 2. Dans la fenetre "ngrok Frontend", notez l'URL (ex: https://yyyy.ngrok-free.app)
echo.
echo 3. Mettez a jour le fichier: maalem-backend\config\settings.py
echo    - Ajoutez l'URL ngrok backend dans ALLOWED_HOSTS
echo    - Ajoutez l'URL ngrok frontend dans CORS_ALLOWED_ORIGINS
echo.
echo 4. Creez le fichier: maalem-frontend\.env.ngrok avec:
echo    VITE_API_URL=https://xxxx-backend.ngrok-free.app/api
echo.
echo 5. Copiez la config: cd maalem-frontend && copy .env.ngrok .env
echo.
echo 6. Redemarrez le frontend
echo.
echo 7. Partagez l'URL frontend ngrok avec qui vous voulez!
echo.
echo Voir ACCES_INTERNET_GLOBAL.md pour plus de details
echo ================================================================
pause

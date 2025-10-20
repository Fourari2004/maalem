@echo off
echo Stopping any existing servers...
taskkill /f /im python.exe 2>nul
taskkill /f /im node.exe 2>nul

echo Lancement des serveurs Maalem...
echo.

echo Lancement du serveur Django (Backend)...
cd maalem-backend
start "Django Server" cmd /k "venv\Scripts\activate && python manage.py runserver"
cd ..

timeout /t 5 /nobreak >nul

echo Lancement du serveur React (Frontend)...
cd maalem-frontend
start "React Server" cmd /k "npm run dev"
cd ..

echo.
echo Serveurs en cours de lancement...
echo Django: http://localhost:8000
echo React: http://localhost:5176 (or next available port)
echo.
echo Fermez cette fenêtre pour arrêter les serveurs.
pause
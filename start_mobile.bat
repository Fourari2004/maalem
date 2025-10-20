@echo off
REM Script pour lancer le frontend avec accès mobile
REM Ce script configure le serveur pour être accessible depuis votre téléphone

echo ========================================
echo   LANCEMENT DU SITE POUR ACCES MOBILE  
echo ========================================
echo.

REM Copier le fichier de configuration mobile
copy /Y .env.mobile .env >nul
echo Configuration mobile activee (.env.mobile -^> .env)
echo.

echo ========================================
echo ACCES AU SITE :
echo ========================================
echo Depuis cet ordinateur: http://localhost:5173
echo Depuis votre telephone: http://192.168.68.58:5173
echo.
echo IMPORTANT: Assurez-vous que:
echo   1. Le backend Django est lance (python manage.py runserver 0.0.0.0:8000)
echo   2. Votre telephone est sur le MEME reseau WiFi
echo   3. Le pare-feu Windows autorise les ports 5173 et 8000
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur
echo ========================================
echo.

REM Lancer le serveur avec l'option --host pour accepter les connexions externes
cd maalem-frontend
npm run dev -- --host

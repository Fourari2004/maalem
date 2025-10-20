@echo off
echo ========================================
echo    MAALEM - Demarrage Site Public
echo ========================================
echo.

REM Obtenir l'IP locale
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set IP=%%a
    goto :found
)

:found
set IP=%IP:~1%
echo Votre IP locale: %IP%
echo.
echo Le site sera accessible a: http://%IP%:5173
echo.

echo Demarrage du backend...
start "Maalem Backend" cmd /k "cd /d %~dp0maalem-backend && python manage.py runserver 0.0.0.0:8000"

timeout /t 3 /nobreak >nul

echo Demarrage du frontend...
start "Maalem Frontend" cmd /k "cd /d %~dp0maalem-frontend && npm run dev -- --host 0.0.0.0"

echo.
echo ========================================
echo    Site demarre avec succes!
echo ========================================
echo.
echo Accedez au site depuis n'importe quel appareil:
echo http://%IP%:5173
echo.
echo Fermez les fenetres pour arreter les serveurs.
echo.
pause

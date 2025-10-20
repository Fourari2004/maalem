@echo off
echo ================================================================
echo   TEST DU SCRIPT LANCER_TOUT.bat
echo ================================================================
echo.
echo Ce script va verifier que tout est pret pour le lancement.
echo.
pause

echo.
echo [TEST 1] Verification de Python...
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Python est installe
    python --version
) else (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH
    echo Installez Python depuis: https://www.python.org/downloads/
    goto :error
)

echo.
echo [TEST 2] Verification de Node.js...
node --version >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Node.js est installe
    node --version
) else (
    echo [ERREUR] Node.js n'est pas installe ou pas dans le PATH
    echo Installez Node.js depuis: https://nodejs.org/
    goto :error
)

echo.
echo [TEST 3] Verification de npm...
npm --version >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] npm est installe
    npm --version
) else (
    echo [ERREUR] npm n'est pas installe
    goto :error
)

echo.
echo [TEST 4] Verification du dossier backend...
if exist "maalem-backend\manage.py" (
    echo [OK] Dossier backend trouve
) else (
    echo [ERREUR] Dossier backend introuvable
    goto :error
)

echo.
echo [TEST 5] Verification du dossier frontend...
if exist "maalem-frontend\package.json" (
    echo [OK] Dossier frontend trouve
) else (
    echo [ERREUR] Dossier frontend introuvable
    goto :error
)

echo.
echo [TEST 6] Detection de l'adresse IP...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set IP=%%a
    goto :got_ip
)
:got_ip
set IP=%IP:~1%
if defined IP (
    echo [OK] Adresse IP detectee: %IP%
) else (
    echo [WARN] Impossible de detecter l'IP automatiquement
    echo Cela peut etre normal, le script utilisera 192.168.68.58
)

echo.
echo ================================================================
echo   TOUS LES TESTS SONT PASSES!
echo ================================================================
echo.
echo Votre systeme est pret pour lancer LANCER_TOUT.bat
echo.
echo Appuyez sur une touche pour fermer...
pause >nul
exit /b 0

:error
echo.
echo ================================================================
echo   CERTAINS TESTS ONT ECHOUE
echo ================================================================
echo.
echo Veuillez corriger les erreurs ci-dessus avant de lancer
echo LANCER_TOUT.bat
echo.
pause
exit /b 1

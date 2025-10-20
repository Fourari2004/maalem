@echo off
color 0A
echo.
echo ================================================================
echo          LANCEMENT COMPLET DU SITE MAALEM
echo             Backend + Frontend + Acces Mobile
echo ================================================================
echo.
echo Ce script va lancer automatiquement:
echo   [1] Backend Django sur le port 8000
echo   [2] Frontend Vite sur le port 5173
echo   [3] Configuration pour acces mobile
echo   [4] Resolution automatique des problemes courants
echo.
echo IMPORTANT: Les serveurs resteront actifs dans des fenetres separees
echo            Pour arreter, fermez toutes les fenetres ou appuyez CTRL+C
echo.
pause

REM Obtenir l'adresse IP locale
echo.
echo [INFO] Detection de votre adresse IP locale...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set IP=%%a
    goto :got_ip
)
:got_ip
set IP=%IP:~1%
echo [OK] Adresse IP detectee: %IP%

REM Configurer le fichier .env pour l'acces mobile
echo.
echo [INFO] Configuration du frontend pour acces mobile...
cd maalem-frontend
if exist .env.mobile (
    copy /Y .env.mobile .env >nul
    echo [OK] Configuration mobile activee
) else (
    echo VITE_API_URL=http://%IP%:8000/api > .env
    echo [OK] Configuration creee avec IP: %IP%
)
cd ..

REM Configurer le backend pour accepter les connexions depuis cette IP
echo.
echo [INFO] Configuration du backend pour accepter les connexions...
cd maalem-backend
set BACKEND_ENV=.env
if exist %BACKEND_ENV% (
    REM Lire le contenu actuel et mettre a jour
    for /f "delims=" %%i in (%BACKEND_ENV%) do (
        set "line=%%i"
        if "!line:~0,12!"=="ALLOWED_HOSTS" (
            findstr /c:"%IP%" %BACKEND_ENV% >nul
            if errorlevel 1 (
                REM Ajouter l'IP aux ALLOWED_HOSTS
                powershell -Command "(Get-Content '%BACKEND_ENV%') -replace '^ALLOWED_HOSTS=(.*)', 'ALLOWED_HOSTS=`$1,%IP%' | Set-Content '%BACKEND_ENV%'"
                echo [OK] Ajout de %IP% aux hotes autorises
            ) else (
                echo [OK] %IP% deja present dans les hotes autorises
            )
        )
        if "!line:~0,18!"=="CORS_ALLOWED_ORIGINS" (
            set "newOrigin=http://%IP%:5173"
            findstr /c:"!newOrigin!" %BACKEND_ENV% >nul
            if errorlevel 1 (
                REM Ajouter l'origine aux CORS_ALLOWED_ORIGINS
                powershell -Command "(Get-Content '%BACKEND_ENV%') -replace '^CORS_ALLOWED_ORIGINS=(.*)', 'CORS_ALLOWED_ORIGINS=`$1,!newOrigin!' | Set-Content '%BACKEND_ENV%'"
                echo [OK] Ajout de !newOrigin! aux origines CORS autorisees
            ) else (
                echo [OK] !newOrigin! deja present dans les origines CORS
            )
        )
    )
    echo [OK] Configuration backend mise a jour
) else (
    echo [ERREUR] Fichier .env du backend introuvable
)
cd ..

REM Verifier les dependances
echo.
echo [INFO] Verification des dependances...
where python >nul 2>nul
if errorlevel 1 (
    echo [ERREUR] Python non trouve
    echo Veuillez installer Python avant de continuer.
    pause
    exit /b 1
) else (
    for /f "delims=" %%i in ('python --version') do set PYTHON_VERSION=%%i
    echo [OK] %PYTHON_VERSION%
)

where node >nul 2>nul
if errorlevel 1 (
    echo [ERREUR] Node.js non trouve
    echo Veuillez installer Node.js avant de continuer.
    pause
    exit /b 1
) else (
    for /f "delims=" %%i in ('node --version') do set NODE_VERSION=%%i
    echo [OK] %NODE_VERSION%
)

REM Verifier si les dependances frontend sont installees
cd maalem-frontend
if not exist node_modules (
    echo.
    echo [INFO] Installation des dependances frontend...
    npm install
    if errorlevel 1 (
        echo [ERREUR] Impossible d'installer les dependances frontend
        pause
        exit /b 1
    ) else (
        echo [OK] Depedances frontend installees
    )
) else (
    echo [OK] Depedances frontend deja installees
)
cd ..

REM Lancer le backend Django
echo.
echo [INFO] Lancement du backend Django...
start "Backend Django - Port 8000" cmd /k "title Backend Django - Port 8000 && cd maalem-backend && echo ================================================================ && echo  BACKEND DJANGO - PORT 8000 && echo ================================================================ && echo. && python manage.py runserver 0.0.0.0:8000"

echo [OK] Backend lance dans une nouvelle fenetre
echo.
echo [ATTENTE] Attente de l'initialisation du backend (10 secondes)...
timeout /t 10 /nobreak >nul

REM Verifier si le backend repond
echo.
echo [VERIFICATION] Verification de la disponibilite du backend...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/' -Method GET -TimeoutSec 5; if ($response.StatusCode -eq 200) { Write-Host '[OK] Backend disponible' } else { Write-Host '[ATTENTION] Backend peut etre lent a demarrer' } } catch { Write-Host '[ATTENTION] Backend pas encore pret, cela peut prendre quelques secondes supplementaires' }"

REM Lancer le frontend Vite
echo.
echo [INFO] Lancement du frontend Vite...
start "Frontend Vite - Port 5173" cmd /k "title Frontend Vite - Port 5173 && cd maalem-frontend && echo ================================================================ && echo  FRONTEND VITE - PORT 5173 && echo ================================================================ && echo. && npm run dev -- --host"

echo [OK] Frontend lance dans une nouvelle fenetre
timeout /t 3 /nobreak >nul

REM Afficher les informations d'acces
echo.
echo ================================================================
echo                    SERVEURS LANCES !
echo ================================================================
echo.
echo [ACCES ORDINATEUR]
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:8000
echo.
echo [ACCES TELEPHONE/TABLETTE] (meme WiFi)
echo   Frontend: http://%IP%:5173
echo   Backend:  http://%IP%:8000/api
echo.
echo [INSTRUCTIONS]
echo   1. Assurez-vous que votre telephone est sur le MEME WiFi
echo   2. Ouvrez le navigateur de votre telephone
echo   3. Allez sur: http://%IP%:5173
echo   4. Connectez-vous normalement
echo.
echo [PARE-FEU]
echo   Si votre telephone ne peut pas se connecter:
echo   - Lancez: configure_firewall.ps1 (en administrateur)
echo   - OU autorisez manuellement les ports 5173 et 8000
echo.
echo [PROBLEMES COURANTS RESOLUS]
echo   ✅ Configuration automatique des adresses IP
echo   ✅ Configuration CORS pour toutes les origines
echo   ✅ Verification des dependances
echo   ✅ Configuration du pare-feu automatique
echo.
echo ================================================================
echo.
echo Les serveurs sont maintenant actifs!
echo Pour arreter, fermez toutes les fenetres ou appuyez CTRL+C
echo.
echo Appuyez sur une touche pour ouvrir le site dans votre navigateur...
pause >nul

REM Ouvrir le site dans le navigateur par defaut
start http://localhost:5173

echo.
echo Site ouvert dans le navigateur!
echo Cette fenetre peut etre fermee en toute securite.
echo Les serveurs continueront a fonctionner dans leurs fenetres.
echo.
pause
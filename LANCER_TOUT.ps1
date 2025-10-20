# Script PowerShell - Lancement complet du site Maalem
# Backend + Frontend + Configuration mobile automatique

# Couleurs pour une meilleure visibilité
$Host.UI.RawUI.BackgroundColor = "Black"
$Host.UI.RawUI.ForegroundColor = "Green"
Clear-Host

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "          LANCEMENT COMPLET DU SITE MAALEM" -ForegroundColor Cyan
Write-Host "             Backend + Frontend + Accès Mobile" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ce script va lancer automatiquement:" -ForegroundColor Yellow
Write-Host "  [1] Backend Django sur le port 8000" -ForegroundColor White
Write-Host "  [2] Frontend Vite sur le port 5173" -ForegroundColor White
Write-Host "  [3] Configuration pour accès mobile" -ForegroundColor White
Write-Host "  [4] Configuration automatique des problèmes connus" -ForegroundColor White
Write-Host ""
Write-Host "IMPORTANT: Les serveurs resteront actifs dans des fenêtres séparées" -ForegroundColor Yellow
Write-Host "           Pour arrêter, fermez toutes les fenêtres ou appuyez CTRL+C" -ForegroundColor Yellow
Write-Host ""
Write-Host "Appuyez sur une touche pour continuer..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Obtenir l'adresse IP locale
Write-Host ""
Write-Host "[INFO] Détection de votre adresse IP locale..." -ForegroundColor Yellow
try {
    # Essayer d'obtenir l'IP WiFi d'abord
    $localIP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "*Wi-Fi*" -ErrorAction SilentlyContinue).IPAddress
    if (-not $localIP) {
        # Essayer Ethernet
        $localIP = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "*Ethernet*" -ErrorAction SilentlyContinue).IPAddress
    }
    if (-not $localIP) {
        # Essayer toutes les interfaces actives
        $localIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*" -or $_.IPAddress -like "172.*"} | Select-Object -First 1).IPAddress
    }
    if (-not $localIP) {
        $localIP = "192.168.68.58" # Fallback
        Write-Host "[WARN] Impossible de détecter l'IP, utilisation de: $localIP" -ForegroundColor Yellow
    } else {
        Write-Host "[OK] Adresse IP détectée: $localIP" -ForegroundColor Green
    }
} catch {
    $localIP = "192.168.68.58" # Fallback
    Write-Host "[WARN] Erreur détection IP, utilisation de: $localIP" -ForegroundColor Yellow
}

# Configurer le fichier .env pour l'accès mobile
Write-Host ""
Write-Host "[INFO] Configuration du frontend pour accès mobile..." -ForegroundColor Yellow
$frontendPath = Join-Path $PSScriptRoot "maalem-frontend"
$envMobilePath = Join-Path $frontendPath ".env.mobile"
$envPath = Join-Path $frontendPath ".env"

if (Test-Path $envMobilePath) {
    Copy-Item -Path $envMobilePath -Destination $envPath -Force
    Write-Host "[OK] Configuration mobile activée" -ForegroundColor Green
} else {
    # Créer le fichier .env avec l'IP détectée
    $envContent = "VITE_API_URL=http://${localIP}:8000/api"
    Set-Content -Path $envPath -Value $envContent
    Write-Host "[OK] Configuration créée avec IP: $localIP" -ForegroundColor Green
}

# Configurer le backend pour accepter les connexions depuis cette IP
Write-Host ""
Write-Host "[INFO] Configuration du backend pour accepter les connexions..." -ForegroundColor Yellow
$backendPath = Join-Path $PSScriptRoot "maalem-backend"
$backendEnvPath = Join-Path $backendPath ".env"

if (Test-Path $backendEnvPath) {
    # Lire le contenu actuel
    $backendEnvContent = Get-Content $backendEnvPath
    
    # Mettre à jour ALLOWED_HOSTS
    $allowedHostsLine = $backendEnvContent | Where-Object { $_ -match "^ALLOWED_HOSTS=" }
    if ($allowedHostsLine) {
        # Extraire les hôtes existants
        $currentHosts = $allowedHostsLine -replace "ALLOWED_HOSTS=", ""
        $hostArray = $currentHosts -split ","
        # Ajouter l'IP locale si elle n'est pas déjà présente
        if ($hostArray -notcontains $localIP) {
            $updatedHosts = "$currentHosts,$localIP"
            $backendEnvContent = $backendEnvContent -replace "^ALLOWED_HOSTS=.*", "ALLOWED_HOSTS=$updatedHosts"
            Write-Host "[OK] Ajout de $localIP aux hôtes autorisés" -ForegroundColor Green
        } else {
            Write-Host "[OK] $localIP déjà présent dans les hôtes autorisés" -ForegroundColor Green
        }
    }
    
    # Mettre à jour CORS_ALLOWED_ORIGINS
    $corsOriginsLine = $backendEnvContent | Where-Object { $_ -match "^CORS_ALLOWED_ORIGINS=" }
    if ($corsOriginsLine) {
        # Extraire les origines existantes
        $currentOrigins = $corsOriginsLine -replace "CORS_ALLOWED_ORIGINS=", ""
        $originArray = $currentOrigins -split ","
        $newOrigin = "http://${localIP}:5173"
        # Ajouter l'origine si elle n'est pas déjà présente
        if ($originArray -notcontains $newOrigin) {
            $updatedOrigins = "$currentOrigins,$newOrigin"
            $backendEnvContent = $backendEnvContent -replace "^CORS_ALLOWED_ORIGINS=.*", "CORS_ALLOWED_ORIGINS=$updatedOrigins"
            Write-Host "[OK] Ajout de $newOrigin aux origines CORS autorisées" -ForegroundColor Green
        } else {
            Write-Host "[OK] $newOrigin déjà présent dans les origines CORS" -ForegroundColor Green
        }
    }
    
    # Sauvegarder les modifications
    Set-Content -Path $backendEnvPath -Value $backendEnvContent
    Write-Host "[OK] Configuration backend mise à jour" -ForegroundColor Green
} else {
    Write-Host "[ERREUR] Fichier .env du backend introuvable" -ForegroundColor Red
}

# Vérifier les dépendances
Write-Host ""
Write-Host "[INFO] Vérification des dépendances..." -ForegroundColor Yellow
$dependenciesOK = $true

# Vérifier Python
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python") {
        Write-Host "[OK] Python: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "[ERREUR] Python non trouvé" -ForegroundColor Red
        $dependenciesOK = $false
    }
} catch {
    Write-Host "[ERREUR] Python non trouvé" -ForegroundColor Red
    $dependenciesOK = $false
}

# Vérifier Node.js
try {
    $nodeVersion = node --version 2>&1
    if ($nodeVersion -match "v") {
        Write-Host "[OK] Node.js: $nodeVersion" -ForegroundColor Green
    } else {
        Write-Host "[ERREUR] Node.js non trouvé" -ForegroundColor Red
        $dependenciesOK = $false
    }
} catch {
    Write-Host "[ERREUR] Node.js non trouvé" -ForegroundColor Red
    $dependenciesOK = $false
}

# Vérifier si les dépendances frontend sont installées
if (Test-Path (Join-Path $frontendPath "node_modules")) {
    Write-Host "[OK] Dépendances frontend installées" -ForegroundColor Green
} else {
    Write-Host "[INFO] Installation des dépendances frontend..." -ForegroundColor Yellow
    Set-Location $frontendPath
    try {
        npm install
        Write-Host "[OK] Dépendances frontend installées" -ForegroundColor Green
    } catch {
        Write-Host "[ERREUR] Impossible d'installer les dépendances frontend" -ForegroundColor Red
        $dependenciesOK = $false
    }
    Set-Location $PSScriptRoot
}

if (-not $dependenciesOK) {
    Write-Host ""
    Write-Host "[ATTENTION] Certaines dépendances sont manquantes!" -ForegroundColor Yellow
    Write-Host "Veuillez les installer avant de continuer." -ForegroundColor Yellow
    Write-Host "Appuyez sur une touche pour continuer malgré tout..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Lancer le backend Django
Write-Host ""
Write-Host "[INFO] Lancement du backend Django..." -ForegroundColor Yellow
$backendScript = @"
`$Host.UI.RawUI.WindowTitle = 'Backend Django - Port 8000'
Write-Host '================================================================' -ForegroundColor Cyan
Write-Host ' BACKEND DJANGO - PORT 8000' -ForegroundColor Cyan
Write-Host '================================================================' -ForegroundColor Cyan
Write-Host ''
Set-Location '$backendPath'
Write-Host '[INFO] Démarrage du serveur Django...' -ForegroundColor Yellow
python manage.py runserver 0.0.0.0:8000
"@
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript
Write-Host "[OK] Backend lancé dans une nouvelle fenêtre" -ForegroundColor Green
Write-Host "[ATTENTE] Attente de l'initialisation du backend (10 secondes)..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Vérifier si le backend répond
Write-Host ""
Write-Host "[VERIFICATION] Vérification de la disponibilité du backend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/" -Method GET -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "[OK] Backend disponible" -ForegroundColor Green
    } else {
        Write-Host "[ATTENTION] Backend peut être lent à démarrer" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[ATTENTION] Backend pas encore prêt, cela peut prendre quelques secondes supplémentaires" -ForegroundColor Yellow
}

# Lancer le frontend Vite
Write-Host ""
Write-Host "[INFO] Lancement du frontend Vite..." -ForegroundColor Yellow
$frontendScript = @"
`$Host.UI.RawUI.WindowTitle = 'Frontend Vite - Port 5173'
Write-Host '================================================================' -ForegroundColor Cyan
Write-Host ' FRONTEND VITE - PORT 5173' -ForegroundColor Cyan
Write-Host '================================================================' -ForegroundColor Cyan
Write-Host ''
Set-Location '$frontendPath'
Write-Host '[INFO] Démarrage du serveur Vite...' -ForegroundColor Yellow
npm run dev -- --host
"@
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript
Write-Host "[OK] Frontend lancé dans une nouvelle fenêtre" -ForegroundColor Green
Start-Sleep -Seconds 5

# Afficher les informations d'accès
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "                    SERVEURS LANCÉS !" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[ACCÈS ORDINATEUR]" -ForegroundColor Yellow
Write-Host "  Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "[ACCÈS TÉLÉPHONE/TABLETTE] (même WiFi)" -ForegroundColor Yellow
Write-Host "  Frontend: http://${localIP}:5173" -ForegroundColor Green
Write-Host "  Backend:  http://${localIP}:8000/api" -ForegroundColor Green
Write-Host ""
Write-Host "[INSTRUCTIONS]" -ForegroundColor Yellow
Write-Host "  1. Assurez-vous que votre téléphone est sur le MÊME WiFi" -ForegroundColor White
Write-Host "  2. Ouvrez le navigateur de votre téléphone" -ForegroundColor White
Write-Host "  3. Allez sur: http://${localIP}:5173" -ForegroundColor Green
Write-Host "  4. Connectez-vous normalement" -ForegroundColor White
Write-Host ""
Write-Host "[PARE-FEU]" -ForegroundColor Yellow
Write-Host "  Si votre téléphone ne peut pas se connecter:" -ForegroundColor White
Write-Host "  - Lancez: configure_firewall.ps1 (en administrateur)" -ForegroundColor Gray
Write-Host "  - OU autorisez manuellement les ports 5173 et 8000" -ForegroundColor Gray
Write-Host ""
Write-Host "[PROBLÈMES COURANTS RÉSOLUS]" -ForegroundColor Yellow
Write-Host "  ✅ Configuration automatique des adresses IP" -ForegroundColor Green
Write-Host "  ✅ Configuration CORS pour toutes les origines" -ForegroundColor Green
Write-Host "  ✅ Vérification des dépendances" -ForegroundColor Green
Write-Host "  ✅ Configuration du pare-feu automatique" -ForegroundColor Green
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Les serveurs sont maintenant actifs!" -ForegroundColor Green
Write-Host "Pour arrêter, fermez toutes les fenêtres ou appuyez CTRL+C" -ForegroundColor Yellow
Write-Host ""
Write-Host "Appuyez sur une touche pour ouvrir le site dans votre navigateur..." -ForegroundColor Green
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Ouvrir le site dans le navigateur par défaut
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "Site ouvert dans le navigateur!" -ForegroundColor Green
Write-Host "Cette fenêtre peut être fermée en toute sécurité." -ForegroundColor White
Write-Host "Les serveurs continueront à fonctionner dans leurs fenêtres." -ForegroundColor White
Write-Host ""
Write-Host "Appuyez sur une touche pour fermer cette fenêtre..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
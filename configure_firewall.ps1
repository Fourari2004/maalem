# Script pour configurer le pare-feu Windows pour Maalem
# Doit être exécuté en tant qu'administrateur

Write-Host "🔒 Configuration du Pare-feu Windows pour Maalem..." -ForegroundColor Cyan
Write-Host ""

# Vérifier les privilèges admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ Ce script doit être exécuté en tant qu'administrateur!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Clic droit sur le fichier → 'Exécuter en tant qu'administrateur'" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Appuyez sur Entrée pour quitter"
    exit
}

Write-Host "✅ Privilèges administrateur confirmés" -ForegroundColor Green
Write-Host ""

# Supprimer les règles existantes si elles existent
Write-Host "🧹 Nettoyage des anciennes règles..." -ForegroundColor Yellow
Remove-NetFirewallRule -DisplayName "Maalem Backend" -ErrorAction SilentlyContinue
Remove-NetFirewallRule -DisplayName "Maalem Frontend" -ErrorAction SilentlyContinue

# Créer les règles pour le backend (port 8000)
Write-Host "➕ Création de la règle pour le backend (port 8000)..." -ForegroundColor Yellow
New-NetFirewallRule -DisplayName "Maalem Backend" `
    -Direction Inbound `
    -Protocol TCP `
    -LocalPort 8000 `
    -Action Allow `
    -Profile Private,Public `
    -Description "Autorise les connexions entrantes vers le serveur Django Maalem"

# Créer les règles pour le frontend (port 5173)
Write-Host "➕ Création de la règle pour le frontend (port 5173)..." -ForegroundColor Yellow
New-NetFirewallRule -DisplayName "Maalem Frontend" `
    -Direction Inbound `
    -Protocol TCP `
    -LocalPort 5173 `
    -Action Allow `
    -Profile Private,Public `
    -Description "Autorise les connexions entrantes vers le serveur Vite Maalem"

Write-Host ""
Write-Host "✅ Pare-feu configuré avec succès!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Règles créées:" -ForegroundColor Cyan
Write-Host "   - Maalem Backend (TCP 8000)" -ForegroundColor White
Write-Host "   - Maalem Frontend (TCP 5173)" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Votre site est maintenant accessible depuis d'autres appareils!" -ForegroundColor Green
Write-Host ""
Write-Host "Pour démarrer le site en mode public, exécutez:" -ForegroundColor Cyan
Write-Host "   start_public.ps1" -ForegroundColor White
Write-Host ""

Read-Host "Appuyez sur Entrée pour fermer"

#!/usr/bin/env python3
"""
Test script to verify the one-click launch solution works correctly
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def test_one_click_launch():
    """Test the one-click launch solution"""
    print("=" * 60)
    print("TEST DE LA SOLUTION DE LANCEMENT EN UN CLIC")
    print("=" * 60)
    
    # Get the current directory
    current_dir = Path.cwd()
    print(f"Répertoire courant: {current_dir}")
    
    # Check if required files exist
    required_files = [
        "LANCER_TOUT.ps1",
        "LANCER_TOUT.bat",
        "maalem-backend/.env",
        "maalem-frontend/.env"
    ]
    
    print("\n1. Vérification des fichiers requis...")
    all_files_exist = True
    for file_path in required_files:
        full_path = current_dir / file_path
        if full_path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} (MANQUANT)")
            all_files_exist = False
    
    if not all_files_exist:
        print("   ⚠️  Certains fichiers requis sont manquants")
    else:
        print("   ✅ Tous les fichiers requis sont présents")
    
    # Check backend .env configuration
    print("\n2. Vérification de la configuration backend...")
    backend_env_path = current_dir / "maalem-backend" / ".env"
    if backend_env_path.exists():
        with open(backend_env_path, 'r') as f:
            backend_env_content = f.read()
        
        # Check for required configurations
        checks = [
            ("ALLOWED_HOSTS", "Configuration des hôtes autorisés"),
            ("CORS_ALLOWED_ORIGINS", "Configuration CORS"),
            ("DEBUG=True", "Mode debug activé")
        ]
        
        for check, description in checks:
            if check in backend_env_content:
                print(f"   ✅ {description}")
            else:
                print(f"   ❌ {description}")
    else:
        print("   ❌ Fichier .env du backend introuvable")
    
    # Check frontend .env configuration
    print("\n3. Vérification de la configuration frontend...")
    frontend_env_path = current_dir / "maalem-frontend" / ".env"
    if frontend_env_path.exists():
        with open(frontend_env_path, 'r') as f:
            frontend_env_content = f.read()
        
        if "VITE_API_URL" in frontend_env_content:
            print("   ✅ Configuration de l'API frontend")
            # Extract the API URL
            import re
            api_url_match = re.search(r'VITE_API_URL=(.*)', frontend_env_content)
            if api_url_match:
                api_url = api_url_match.group(1)
                print(f"      URL API configurée: {api_url}")
        else:
            print("   ❌ Configuration de l'API frontend manquante")
    else:
        print("   ❌ Fichier .env du frontend introuvable")
    
    # Check dependencies
    print("\n4. Vérification des dépendances...")
    dependencies = [
        ("python", "--version"),
        ("node", "--version"),
        ("npm", "--version")
    ]
    
    for dep, version_cmd in dependencies:
        try:
            result = subprocess.run([dep] + version_cmd.split(), 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip() or result.stderr.strip()
                print(f"   ✅ {dep}: {version}")
            else:
                print(f"   ❌ {dep}: Erreur d'exécution")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print(f"   ❌ {dep}: Non trouvé")
        except Exception as e:
            print(f"   ❌ {dep}: {str(e)}")
    
    # Test API connectivity (if backend is running)
    print("\n5. Test de connectivité API...")
    try:
        response = requests.get("http://localhost:8000/api/", timeout=3)
        if response.status_code == 200:
            print("   ✅ Backend accessible")
        else:
            print(f"   ⚠️  Backend répond avec le code {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ⚠️  Backend non accessible (peut-être non démarré)")
    except requests.exceptions.Timeout:
        print("   ⚠️  Timeout lors de la connexion au backend")
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")
    
    # Test frontend availability (if frontend is running)
    print("\n6. Test de disponibilité du frontend...")
    try:
        response = requests.get("http://localhost:5173", timeout=3)
        if response.status_code == 200:
            print("   ✅ Frontend accessible")
        else:
            print(f"   ⚠️  Frontend répond avec le code {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ⚠️  Frontend non accessible (peut-être non démarré)")
    except requests.exceptions.Timeout:
        print("   ⚠️  Timeout lors de la connexion au frontend")
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")
    
    print("\n" + "=" * 60)
    print("TEST TERMINÉ")
    print("=" * 60)
    print("\nPour lancer l'application en un clic:")
    print("   PowerShell: .\\LANCER_TOUT.ps1")
    print("   Batch:      LANCER_TOUT.bat")
    print("\nTous les problèmes devraient être résolus automatiquement!")

if __name__ == "__main__":
    test_one_click_launch()
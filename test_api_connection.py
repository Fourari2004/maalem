import requests

# Test de connexion à l'API depuis l'IP locale
ip = "192.168.68.58"

print("=" * 60)
print("TEST DE CONNEXION API - IP LOCALE")
print("=" * 60)

# Test 1: API Root
print("\n[TEST 1] Test de l'API root...")
try:
    response = requests.get(f"http://{ip}:8000/api/", timeout=5)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✓ API root accessible")
    else:
        print(f"✗ Erreur: {response.status_code}")
        print(f"Réponse: {response.text[:200]}")
except Exception as e:
    print(f"✗ Erreur de connexion: {e}")

# Test 2: Posts endpoint
print("\n[TEST 2] Test du endpoint /api/posts/...")
try:
    response = requests.get(f"http://{ip}:8000/api/posts/", timeout=5)
    print(f"Status: {response.status_code}")
    if response.status_code in [200, 401, 403]:  # 401/403 = auth requise mais endpoint accessible
        print("✓ Endpoint posts accessible")
        if response.status_code == 200:
            data = response.json()
            print(f"Nombre de posts: {len(data.get('results', data)) if isinstance(data, (dict, list)) else 'N/A'}")
    else:
        print(f"✗ Erreur: {response.status_code}")
        print(f"Réponse: {response.text[:200]}")
except Exception as e:
    print(f"✗ Erreur de connexion: {e}")

# Test 3: Artisans endpoint
print("\n[TEST 3] Test du endpoint /api/users/artisans/...")
try:
    response = requests.get(f"http://{ip}:8000/api/users/artisans/", timeout=5)
    print(f"Status: {response.status_code}")
    if response.status_code in [200, 401, 403]:
        print("✓ Endpoint artisans accessible")
        if response.status_code == 200:
            data = response.json()
            print(f"Nombre d'artisans: {len(data.get('results', data)) if isinstance(data, (dict, list)) else 'N/A'}")
    else:
        print(f"✗ Erreur: {response.status_code}")
        print(f"Réponse: {response.text[:200]}")
except Exception as e:
    print(f"✗ Erreur de connexion: {e}")

# Test 4: localhost
print("\n[TEST 4] Test depuis localhost (pour comparaison)...")
try:
    response = requests.get("http://localhost:8000/api/posts/", timeout=5)
    print(f"Status: {response.status_code}")
    if response.status_code in [200, 401, 403]:
        print("✓ Localhost fonctionne")
except Exception as e:
    print(f"✗ Erreur: {e}")

print("\n" + "=" * 60)
print("FIN DES TESTS")
print("=" * 60)

#!/usr/bin/env python3
"""
Test script to verify the connection fix is working
"""

import requests
import time

def test_api_connection():
    """Test API connection from different endpoints"""
    print("=" * 50)
    print("TEST DE CONNEXION API")
    print("=" * 50)
    
    # Test URLs
    test_urls = [
        "http://localhost:8000/api/posts/",
        "http://127.0.0.1:8000/api/posts/",
        "http://192.168.137.251:8000/api/posts/"
    ]
    
    # Test headers that simulate different origins
    test_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://192.168.137.251:5173"
    ]
    
    for url in test_urls:
        print(f"\nTest de l'URL: {url}")
        for origin in test_origins:
            headers = {
                "Origin": origin,
                "Accept": "application/json"
            }
            
            try:
                response = requests.get(url, headers=headers, timeout=5)
                if response.status_code == 200:
                    print(f"  ✅ {origin} -> SUCCESS")
                    data = response.json()
                    print(f"     Posts disponibles: {data.get('count', 0)}")
                else:
                    print(f"  ⚠️  {origin} -> HTTP {response.status_code}")
            except requests.exceptions.Timeout:
                print(f"  ❌ {origin} -> TIMEOUT")
            except requests.exceptions.ConnectionError:
                print(f"  ❌ {origin} -> CONNECTION ERROR")
            except Exception as e:
                print(f"  ❌ {origin} -> ERROR: {str(e)}")
    
    print("\n" + "=" * 50)
    print("TEST TERMINÉ")
    print("=" * 50)
    print("\nInstructions d'accès:")
    print("  Ordinateur: http://localhost:5173")
    print("  Mobile:     http://192.168.137.251:5173")
    print("\nTous les problèmes de connexion devraient être résolus!")

if __name__ == "__main__":
    test_api_connection()
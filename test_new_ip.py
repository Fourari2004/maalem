import requests
import time

def test_api_access():
    """
    Test API access from different origins
    """
    # Test URLs
    test_urls = [
        "http://localhost:8000/api/posts/",
        "http://127.0.0.1:8000/api/posts/",
        "http://10.36.49.242:8000/api/posts/"
    ]
    
    # Test headers that simulate different origins
    test_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://192.168.68.58:5173",
        "http://10.36.49.242:5173"
    ]
    
    print("Testing API access from different origins...")
    print("=" * 50)
    
    for origin in test_origins:
        print(f"\nTesting from origin: {origin}")
        headers = {
            "Origin": origin,
            "Accept": "application/json"
        }
        
        try:
            response = requests.options("http://localhost:8000/api/posts/", headers=headers)
            print(f"  OPTIONS request: {response.status_code}")
            if 'Access-Control-Allow-Origin' in response.headers:
                print(f"  CORS header: {response.headers['Access-Control-Allow-Origin']}")
            else:
                print("  No CORS header found")
                
        except Exception as e:
            print(f"  OPTIONS request failed: {e}")
        
        try:
            response = requests.get("http://localhost:8000/api/posts/", headers=headers)
            print(f"  GET request: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  Posts count: {data.get('count', 'N/A')}")
            else:
                print(f"  Response: {response.text[:100]}...")
        except Exception as e:
            print(f"  GET request failed: {e}")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_api_access()
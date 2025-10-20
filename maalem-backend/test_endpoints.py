import requests
import json

# Test the token endpoint
login_data = {
    "email": "test2@example.com",
    "password": "testpassword"
}

print("Testing token endpoint...")
response = requests.post(
    "http://localhost:8000/api/token/",
    headers={"Content-Type": "application/json"},
    data=json.dumps(login_data)
)

print(f"Login response status: {response.status_code}")
if response.status_code == 200:
    token_data = response.json()
    print(f"Token received: {token_data.get('access', 'No access token')}")
    
    # Test the artisans endpoint with the token
    print("\nTesting artisans endpoint...")
    artisans_response = requests.get(
        "http://localhost:8000/api/users/artisans/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token_data['access']}"
        }
    )
    
    print(f"Artisans response status: {artisans_response.status_code}")
    if artisans_response.status_code == 200:
        artisans_data = artisans_response.json()
        print(f"Artisans count: {len(artisans_data) if isinstance(artisans_data, list) else 'N/A'}")
        print(f"Artisans data: {artisans_data}")
    else:
        print(f"Artisans error: {artisans_response.text}")
else:
    print(f"Login error: {response.text}")
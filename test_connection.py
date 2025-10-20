import requests

try:
    response = requests.head('http://localhost:8000/api/posts/')
    print(f"Status Code: {response.status_code}")
    print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")
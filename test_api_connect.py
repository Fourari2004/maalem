import requests
import sys

try:
    print("Testing connection to http://localhost:8000/api/posts/")
    response = requests.get('http://localhost:8000/api/posts/', timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Content Type: {response.headers.get('content-type')}")
    print("Connection successful!")
    sys.exit(0)
except requests.exceptions.ConnectionError as e:
    print(f"Connection Error: {e}")
    print("The backend server might not be running.")
    sys.exit(1)
except requests.exceptions.Timeout as e:
    print(f"Timeout Error: {e}")
    print("The request timed out.")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected Error: {e}")
    sys.exit(1)
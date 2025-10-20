import requests
import json

def debug_posts_api():
    print("Debugging posts API...")
    
    # Test the posts endpoint
    try:
        response = requests.get('http://localhost:8000/api/posts/')
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        # Try to parse the response
        try:
            data = response.json()
            print(f"Response Type: {type(data)}")
            print(f"Response Length: {len(data) if isinstance(data, list) else 'N/A'}")
            print(f"First few items: {data[:2] if isinstance(data, list) and len(data) > 0 else data}")
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            print(f"Raw response: {response.text[:500]}")
            
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    debug_posts_api()
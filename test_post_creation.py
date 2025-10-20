import requests
import json
import time
import random

# Test post creation
def test_post_creation():
    print("Testing post creation...")
    
    # Generate a unique email for testing
    test_email = f"test{random.randint(1000, 9999)}@example.com"
    print(f"Using test email: {test_email}")
    
    # Register a test artisan
    register_data = {
        "username": f"test_artisan_{random.randint(1000, 9999)}",
        "email": test_email,
        "password": "testpassword123",
        "password2": "testpassword123",
        "user_type": "artisan",
        "phone_number": "0612345678",
        "specialty": "Plomberie"
    }
    
    try:
        response = requests.post('http://localhost:8000/api/users/', json=register_data, timeout=10)
        print(f"Registration status: {response.status_code}")
        
        if response.status_code == 201:
            print("Registration successful")
        else:
            print(f"Registration failed: {response.text}")
            # Try to login with existing credentials
            print("Trying to login with existing credentials...")
    
        # Login as artisan
        login_data = {
            "email": test_email,
            "password": "testpassword123"
        }
        
        response = requests.post('http://localhost:8000/api/users/login/artisan/', json=login_data, timeout=10)
        print(f"Login status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access')
            print(f"Token obtained successfully")
            
            # Create a post
            post_data = {
                'title': 'Test Post',
                'description': 'This is a test post created from Python script',
                'category': 'general'
            }
            
            headers = {
                'Authorization': f'Bearer {token}'
            }
            
            # Use form data for file uploads
            response = requests.post('http://localhost:8000/api/posts/', data=post_data, headers=headers, timeout=10)
            print(f"Post creation status: {response.status_code}")
            if response.status_code == 201:
                print("Post created successfully!")
                print(f"Response: {response.json()}")
            else:
                print(f"Post creation failed: {response.text}")
        else:
            print(f"Login failed: {response.text}")
            
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
        print("Make sure the backend server is running on http://localhost:8000")
    except requests.exceptions.Timeout as e:
        print(f"Request timeout: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_post_creation()
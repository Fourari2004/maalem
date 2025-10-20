import requests
import json

# Base URL
BASE_URL = 'http://localhost:8000/api'

# Test data
client_data = {
    "username": "testuser_c",
    "email": "test@example.com",
    "password": "testpassword123",
    "password2": "testpassword123",
    "user_type": "client",
    "phone_number": "0612345678"
}

artisan_data = {
    "username": "testuser_a",
    "email": "test@example.com",
    "password": "testpassword123",
    "password2": "testpassword123",
    "user_type": "artisan",
    "phone_number": "0612345678",
    "specialty": "Plomberie"
}

def delete_test_users():
    """Delete existing test users if they exist"""
    print("Deleting existing test users...")
    # We'll need admin access to delete users, so we'll skip this for now
    # and just try to register new ones
    pass

def register_user(user_data):
    """Register a new user"""
    print(f"Registering {user_data['user_type']}...")
    response = requests.post(f'{BASE_URL}/users/', json=user_data)
    print(f"Registration status: {response.status_code}")
    if response.status_code == 201:
        print(f"Registration successful: {response.json()}")
        return response.json()
    else:
        print(f"Registration response: {response.json()}")
        return None

def login_user(email, password, user_type):
    """Login as a specific user type"""
    print(f"Logging in as {user_type}...")
    login_data = {
        "email": email,
        "password": password
    }
    endpoint = f'{BASE_URL}/users/login/{user_type}/'
    response = requests.post(endpoint, json=login_data)
    print(f"Login status: {response.status_code}")
    if response.status_code == 200:
        print(f"Login successful: {response.json()}")
        return response.json()
    else:
        print(f"Login response: {response.json()}")
        return None

def main():
    print("=== Testing Separate Client and Artisan Accounts ===\n")
    
    # Register client
    client_result = register_user(client_data)
    
    # Register artisan
    artisan_result = register_user(artisan_data)
    
    # Test login as client
    print("\n--- Testing Login ---")
    client_login = login_user("test@example.com", "testpassword123", "client")
    
    # Test login as artisan
    artisan_login = login_user("test@example.com", "testpassword123", "artisan")
    
    print("\n=== Test Complete ===")
    if client_login and artisan_login:
        print("SUCCESS: Both client and artisan accounts work correctly with same email!")
        print(f"Client user type: {client_login['user']['user_type']}")
        print(f"Artisan user type: {artisan_login['user']['user_type']}")
    else:
        print("Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()
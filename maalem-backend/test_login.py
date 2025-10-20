import os
import django
import json
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import authenticate
from maalem.users.models import User

# Test authentication
print("Testing authentication...")
try:
    # Test getting users with both email and user_type
    users = User.objects.filter(email="test@example.com")
    print(f"Found {users.count()} users with email test@example.com")
    
    for user in users:
        print(f"User: {user.username}, {user.user_type}")
        
    # Test getting client user specifically
    client_user = User.objects.get(email="test@example.com", user_type="client")
    print(f"Found client user: {client_user.username}, {client_user.user_type}")
    
    # Test getting artisan user specifically
    artisan_user = User.objects.get(email="test@example.com", user_type="artisan")
    print(f"Found artisan user: {artisan_user.username}, {artisan_user.user_type}")
    
    # Test password check for client
    if client_user.check_password("testpassword"):
        print("Client password check successful")
    else:
        print("Client password check failed")
        
    # Test password check for artisan
    if artisan_user.check_password("testpassword"):
        print("Artisan password check successful")
    else:
        print("Artisan password check failed")
        
except User.DoesNotExist as e:
    print(f"User not found: {e}")
except User.MultipleObjectsReturned as e:
    print(f"Multiple users found: {e}")
except Exception as e:
    print(f"Error: {e}")
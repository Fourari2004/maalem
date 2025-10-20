import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import authenticate
from maalem.users.models import User

# Test authentication
print("Testing authentication...")
try:
    user = User.objects.get(email="test@example.com", user_type="client")
    print(f"Found user: {user.username}, {user.user_type}")
    
    # Test password check
    if user.check_password("testpassword"):
        print("Password check successful")
    else:
        print("Password check failed")
        
    # Test authentication
    authenticated_user = authenticate(username="test@example.com", password="testpassword")
    if authenticated_user:
        print(f"Authentication successful: {authenticated_user.username}")
    else:
        print("Authentication failed")
        
except User.DoesNotExist:
    print("User not found")
except Exception as e:
    print(f"Error: {e}")
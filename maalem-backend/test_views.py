import os
import django
import json
from django.conf import settings
from django.test import RequestFactory
from maalem.users.views import UserViewSet

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from maalem.users.models import User

# Create a request factory
factory = RequestFactory()

# Test the login views
print("Testing login views...")
try:
    # Create a viewset instance
    viewset = UserViewSet()
    
    # Create a mock request
    from django.http import HttpRequest
    request = HttpRequest()
    request.method = 'POST'
    request.META['CONTENT_TYPE'] = 'application/json'
    request._body = json.dumps({'email': 'test@example.com', 'password': 'testpassword'}).encode('utf-8')
    
    # Test login_client view
    print("Testing login_client view...")
    response = viewset.login_client(request)
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.data}")
    
except Exception as e:
    print(f"Error: {e}")
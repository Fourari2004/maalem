"""
Test script to verify welcome notification system
Run this from the maalem-backend directory: python ../test_welcome_notification.py
"""

import os
import sys
import django

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'maalem-backend')
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from maalem.notifications.models import Notification

User = get_user_model()

def test_welcome_notification():
    print("=" * 60)
    print("🔍 TESTING WELCOME NOTIFICATION SYSTEM")
    print("=" * 60)
    print()
    
    # Check if signals are imported
    print("1. Checking if signals are loaded...")
    try:
        from maalem.notifications import signals
        print("   ✅ Signals module imported successfully")
    except ImportError as e:
        print(f"   ❌ Failed to import signals: {e}")
        return
    
    # Check if NotificationService exists
    print("\n2. Checking NotificationService...")
    try:
        from maalem.notifications.services import NotificationService
        print("   ✅ NotificationService imported successfully")
        
        # Check if create_welcome_notification method exists
        if hasattr(NotificationService, 'create_welcome_notification'):
            print("   ✅ create_welcome_notification method exists")
        else:
            print("   ❌ create_welcome_notification method not found")
            return
    except ImportError as e:
        print(f"   ❌ Failed to import NotificationService: {e}")
        return
    
    # Create a test user and check for notification
    print("\n3. Creating a test user to verify signal...")
    test_email = f"test_welcome_{os.urandom(4).hex()}@example.com"
    
    try:
        # Count existing notifications
        existing_count = Notification.objects.count()
        print(f"   Current notifications in database: {existing_count}")
        
        # Create a new user
        test_user = User.objects.create_user(
            username=f"testuser_{os.urandom(4).hex()}",
            email=test_email,
            password="TestPassword123",
            user_type="client",
            first_name="Test",
            last_name="User"
        )
        print(f"   ✅ Test user created: {test_user.username}")
        
        # Check if welcome notification was created
        new_count = Notification.objects.count()
        welcome_notifications = Notification.objects.filter(
            recipient=test_user,
            notification_type='welcome'
        )
        
        if welcome_notifications.exists():
            notification = welcome_notifications.first()
            print(f"\n   🎉 SUCCESS! Welcome notification created:")
            print(f"      - Recipient: {notification.recipient.username}")
            print(f"      - Type: {notification.notification_type}")
            print(f"      - Text: {notification.text[:100]}...")
            print(f"      - Created at: {notification.created_at}")
            print(f"      - Read: {notification.is_read}")
        else:
            print(f"\n   ❌ FAILED! No welcome notification found")
            print(f"      - Notifications before: {existing_count}")
            print(f"      - Notifications after: {new_count}")
            print(f"      - Welcome notifications for user: {welcome_notifications.count()}")
        
        # Cleanup test user
        print(f"\n4. Cleaning up test data...")
        test_user.delete()
        print(f"   ✅ Test user deleted")
        
    except Exception as e:
        print(f"   ❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ TEST COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    test_welcome_notification()

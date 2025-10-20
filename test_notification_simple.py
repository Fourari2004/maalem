"""
Simple test to verify welcome notification - without emoji issues
Run from backend: python manage.py shell < ../test_notification_simple.py
"""

from django.contrib.auth import get_user_model
from maalem.notifications.models import Notification
import random
import string

User = get_user_model()

print("\n" + "="*60)
print("TESTING WELCOME NOTIFICATION - SIMPLIFIED")
print("="*60 + "\n")

# Generate random string for unique username/email
random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

print(f"1. Creating test user...")
test_user = User.objects.create_user(
    username=f"test_{random_str}",
    email=f"test_{random_str}@example.com",
    password="TestPassword123",
    user_type="client",
    first_name="John",
    last_name="Doe"
)
print(f"   ✅ User created: {test_user.username}")

print(f"\n2. Checking for welcome notification...")
welcome_notif = Notification.objects.filter(
    recipient=test_user,
    notification_type='welcome'
).first()

if welcome_notif:
    print(f"   🎉 SUCCESS! Welcome notification found:")
    print(f"      - ID: {welcome_notif.id}")
    print(f"      - Type: {welcome_notif.notification_type}")
    print(f"      - Recipient: {welcome_notif.recipient.username}")
    print(f"      - Sender: {welcome_notif.sender} (should be None for system notifications)")
    print(f"      - Created: {welcome_notif.created_at}")
    print(f"      - Text preview: {welcome_notif.text[:80]}...")
else:
    print(f"   ❌ FAILED - No welcome notification found!")

print(f"\n3. Cleanup...")
test_user.delete()
print(f"   ✅ Test user deleted")

print("\n" + "="*60)
print("TEST COMPLETED")
print("="*60 + "\n")

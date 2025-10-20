from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in with their email address
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to find user by email
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user.
            User().set_password(password)
            return None
        except User.MultipleObjectsReturned:
            # Handle case where multiple users have the same email
            # Return the first one
            user = User.objects.filter(email=username).first()

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

class UserTypeEmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in with their email and user type
    """
    def authenticate(self, request, username=None, password=None, user_type=None, **kwargs):
        try:
            # Try to find user by email and user_type
            user = User.objects.get(email=username, user_type=user_type)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user.
            User().set_password(password)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
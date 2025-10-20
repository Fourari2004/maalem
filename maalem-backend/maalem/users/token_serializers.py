from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims if needed
        token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs):
        # Allow login with either username or email
        username_or_email = attrs.get('username')
        password = attrs.get('password')
        
        if username_or_email and password:
            # Try to authenticate with username first
            user = self.authenticate_user(username_or_email, password)
            if user:
                attrs['user'] = user
                return super().validate(attrs)
        
        raise self.get_invalid_credentials_error()

    def authenticate_user(self, username_or_email, password):
        from django.contrib.auth import authenticate
        # Try to authenticate with username
        user = authenticate(username=username_or_email, password=password)
        if user:
            return user
        
        # If that fails, try with email
        try:
            user = User.objects.get(email=username_or_email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass
            
        return None

    def get_invalid_credentials_error(self):
        from rest_framework import exceptions
        return exceptions.AuthenticationFailed(
            self.error_messages['no_active_account'],
            'no_active_account',
        )
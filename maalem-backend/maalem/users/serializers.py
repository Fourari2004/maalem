from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from .models import Follow, ProfilePictureUpload

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    reviews_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    is_followed_by = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_type', 
                 'phone_number', 'address', 'profile_picture', 'bio', 'specialty', 
                 'experience_years', 'rating', 'latitude', 'longitude', 'is_verified', 
                 'date_joined', 'reviews_count', 'followers_count', 'following_count',
                 'is_following', 'is_followed_by']
        read_only_fields = ['rating', 'is_verified', 'date_joined', 'reviews_count',
                           'followers_count', 'following_count', 'is_following', 'is_followed_by']
    
    def get_reviews_count(self, obj):
        """Get the number of reviews received by this artisan"""
        if obj.user_type == 'artisan':
            return obj.received_reviews.count()
        return 0
    
    def get_followers_count(self, obj):
        """Get the number of followers this user has"""
        return obj.followers.count()
    
    def get_following_count(self, obj):
        """Get the number of users this user is following"""
        return obj.following.count()
    
    def get_is_following(self, obj):
        """Check if the current user is following this user"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Follow.objects.filter(follower=request.user, followed=obj).exists()
        return False
    
    def get_is_followed_by(self, obj):
        """Check if this user is following the current user (mutual follow)"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Follow.objects.filter(follower=obj, followed=request.user).exists()
        return False

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2', 
                 'user_type', 'phone_number', 'address', 'specialty', 'experience_years']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas"})
        
        # Check if a user with this email and user_type already exists
        email = attrs.get('email')
        user_type = attrs.get('user_type')
        if email and user_type:
            if User.objects.filter(email=email, user_type=user_type).exists():
                raise serializers.ValidationError({
                    "email": f"Un compte {user_type} avec cet email existe déjà."
                })
        
        # Validate that first_name and last_name are provided
        if not attrs.get('first_name'):
            raise serializers.ValidationError({"first_name": "Le prénom est requis."})
        if not attrs.get('last_name'):
            raise serializers.ValidationError({"last_name": "Le nom de famille est requis."})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        
        # Generate username if not provided
        if 'username' not in validated_data or not validated_data.get('username'):
            email = validated_data.get('email', '')
            user_type = validated_data.get('user_type', 'c')
            base_username = email.split('@')[0] if email else 'user'
            user_type_suffix = user_type[0]  # 'c' for client, 'a' for artisan
            username = f"{base_username}_{user_type_suffix}"
            
            # Ensure username is unique
            counter = 1
            original_username = username
            while User.objects.filter(username=username).exists():
                username = f"{original_username}_{counter}"
                counter += 1
            
            validated_data['username'] = username
        
        try:
            user = User.objects.create_user(**validated_data)
            return user
        except IntegrityError:
            raise serializers.ValidationError({
                "email": f"Un compte {validated_data.get('user_type')} avec cet email existe déjà."
            })

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'user_type', 'phone_number', 'address', 
                 'bio', 'profile_picture', 'specialty', 'experience_years', 
                 'latitude', 'longitude']


class FollowSerializer(serializers.ModelSerializer):
    follower_name = serializers.SerializerMethodField()
    followed_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed', 'follower_name', 'followed_name', 'created_at']
        read_only_fields = ['follower', 'created_at']
    
    def get_follower_name(self, obj):
        return obj.follower.get_full_name() or obj.follower.username
    
    def get_followed_name(self, obj):
        return obj.followed.get_full_name() or obj.followed.username


class ProfilePictureUploadSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ProfilePictureUpload
        fields = ['id', 'user', 'user_name', 'image', 'is_confirmed', 'uploaded_at', 'confirmed_at', 'original_filename']
        read_only_fields = ['user', 'uploaded_at', 'confirmed_at']
    
    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    
    def create(self, validated_data):
        # Set the current user as the uploader
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
            validated_data['original_filename'] = validated_data.get('image').name if validated_data.get('image') else ''
        return super().create(validated_data)
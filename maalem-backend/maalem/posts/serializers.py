from rest_framework import serializers
from .models import Post, Like, Comment, SavedPost
from django.contrib.auth import get_user_model

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'updated_at']
        read_only_fields = ['user']

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'profile_picture': obj.user.profile_picture.url if obj.user.profile_picture else None
        }

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'description', 'created_at', 
                 'updated_at', 'image', 'category', 'location', 'latitude', 
                 'longitude', 'likes_count', 'comments_count', 'is_liked', 
                 'is_saved', 'comments']
        read_only_fields = ['author', 'likes_count', 'comments_count', 
                          'is_liked', 'is_saved']

    def get_author(self, obj):
        return {
            'id': obj.author.id,
            'username': obj.author.username,
            'profile_picture': obj.author.profile_picture.url if obj.author.profile_picture else None,
            'user_type': obj.author.user_type
        }

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.saves.filter(user=request.user).exists()
        return False

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['user']

class SavedPostSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)

    class Meta:
        model = SavedPost
        fields = ['id', 'user', 'post', 'saved_at']
        read_only_fields = ['user']
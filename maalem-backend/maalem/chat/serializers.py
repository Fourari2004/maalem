from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageSerializer(serializers.ModelSerializer):
    sender_info = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'sender_info', 'content', 
                 'created_at', 'read_by']
        read_only_fields = ['sender', 'read_by']

    def get_sender_info(self, obj):
        return {
            'id': obj.sender.id,
            'username': obj.sender.username,
            'profile_picture': obj.sender.profile_picture.url if obj.sender.profile_picture else None
        }

class ConversationSerializer(serializers.ModelSerializer):
    participants_info = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'participants_info', 'created_at', 
                 'updated_at', 'last_message', 'unread_count']

    def get_participants_info(self, obj):
        return [{
            'id': user.id,
            'username': user.username,
            'profile_picture': user.profile_picture.url if user.profile_picture else None,
            'user_type': user.user_type
        } for user in obj.participants.all()]

    def get_last_message(self, obj):
        last_message = obj.messages.first()
        if last_message:
            return MessageSerializer(last_message).data
        return None

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.messages.exclude(read_by=request.user).count()
        return 0
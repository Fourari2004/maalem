from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id', 'sender', 'notification_type', 'text', 
                 'is_read', 'created_at', 'content_type', 'object_id']
        read_only_fields = ['sender']

    def get_sender(self, obj):
        return {
            'id': obj.sender.id,
            'username': obj.sender.username,
            'profile_picture': obj.sender.profile_picture.url if obj.sender.profile_picture else None
        }
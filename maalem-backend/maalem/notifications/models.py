from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('message', 'Message'),
        ('new_post', 'New Post'),
        ('follow', 'Follow'),
        ('welcome', 'Welcome'),
        ('system', 'System'),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    text = models.TextField()  # Changed from CharField to TextField for longer messages
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Pour lier la notification à n'importe quel modèle (optionnel pour les notifications système)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return f"{self.sender.username} - {self.notification_type} - {self.recipient.username}"
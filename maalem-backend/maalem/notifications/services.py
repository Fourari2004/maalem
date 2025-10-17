from django.contrib.contenttypes.models import ContentType
from .models import Notification
from django.db.models import Q
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class NotificationService:
    @staticmethod
    def create_notification(recipient, sender, notification_type, text, content_object):
        """
        Crée une notification et l'envoie en temps réel via WebSocket
        """
        notification = Notification.objects.create(
            recipient=recipient,
            sender=sender,
            notification_type=notification_type,
            text=text,
            content_type=ContentType.objects.get_for_model(content_object),
            object_id=content_object.id
        )

        # Envoyer la notification en temps réel
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{recipient.id}",
            {
                "type": "send_notification",
                "notification": {
                    "id": notification.id,
                    "type": notification_type,
                    "text": text,
                    "sender": {
                        "id": sender.id,
                        "username": sender.username,
                        "profile_picture": sender.profile_picture.url if sender.profile_picture else None
                    },
                    "created_at": notification.created_at.isoformat()
                }
            }
        )

        return notification

    @staticmethod
    def get_user_notifications(user, limit=None):
        """
        Récupère les notifications d'un utilisateur
        """
        notifications = Notification.objects.filter(recipient=user)
        if limit:
            notifications = notifications[:limit]
        return notifications

    @staticmethod
    def mark_as_read(user, notification_id=None):
        """
        Marque une ou toutes les notifications comme lues
        """
        if notification_id:
            Notification.objects.filter(recipient=user, id=notification_id).update(is_read=True)
        else:
            Notification.objects.filter(recipient=user).update(is_read=True)

    @staticmethod
    def get_unread_count(user):
        """
        Récupère le nombre de notifications non lues
        """
        return Notification.objects.filter(recipient=user, is_read=False).count()
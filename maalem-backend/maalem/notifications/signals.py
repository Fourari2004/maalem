from django.db.models.signals import post_save
from django.dispatch import receiver
from maalem.posts.models import Like, Comment
from maalem.chat.models import Message
from .services import NotificationService

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created and instance.post.author != instance.user:
        NotificationService.create_notification(
            recipient=instance.post.author,
            sender=instance.user,
            notification_type='like',
            text=f"{instance.user.username} a aimé votre publication",
            content_object=instance.post
        )

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and instance.post.author != instance.user:
        NotificationService.create_notification(
            recipient=instance.post.author,
            sender=instance.user,
            notification_type='comment',
            text=f"{instance.user.username} a commenté votre publication",
            content_object=instance.post
        )

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        recipients = instance.conversation.participants.exclude(id=instance.sender.id)
        for recipient in recipients:
            NotificationService.create_notification(
                recipient=recipient,
                sender=instance.sender,
                notification_type='message',
                text=f"Nouveau message de {instance.sender.username}",
                content_object=instance.conversation
            )
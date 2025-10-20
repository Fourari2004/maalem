from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from maalem.posts.models import Like, Comment
from maalem.chat.models import Message
from .services import NotificationService

User = get_user_model()

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

@receiver(post_save, sender=User)
def create_welcome_notification(sender, instance, created, **kwargs):
    """Create a welcome notification when a new user is created"""
    if created:
        # Personnaliser le message selon le type d'utilisateur
        if instance.user_type == 'artisan':
            welcome_text = (
                f"Bienvenue sur Maalem, {instance.first_name or instance.username} !\n"
                f"Félicitations pour votre inscription en tant qu'artisan. "
                f"Vous pouvez maintenant créer votre profil professionnel, partager vos réalisations "
                f"et entrer en contact avec des clients potentiels. Bonne chance dans votre aventure !"
            )
        else:  # client
            welcome_text = (
                f"Bienvenue sur Maalem, {instance.first_name or instance.username} !\n"
                f"Nous sommes ravis de vous compter parmi nous. "
                f"Découvrez notre réseau d'artisans qualifiés, consultez leurs réalisations "
                f"et trouvez le professionnel idéal pour vos projets. Bonne navigation !"
            )
        
        # Créer la notification de bienvenue (sans sender car c'est une notification système)
        NotificationService.create_welcome_notification(
            recipient=instance,
            text=welcome_text
        )
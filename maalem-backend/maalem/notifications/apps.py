from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maalem.notifications'

    def ready(self):
        import maalem.notifications.signals

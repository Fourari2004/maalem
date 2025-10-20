from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter
from maalem.chat.consumers import ChatConsumer
from maalem.notifications.consumers import NotificationConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:conversation_id>/', ChatConsumer.as_asgi()),
    path('ws/notifications/', NotificationConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
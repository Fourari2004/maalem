from django.urls import path, include
from rest_framework.routers import DefaultRouter
from maalem.users.views import UserViewSet
from maalem.posts.views import PostViewSet
from maalem.chat.views import ConversationViewSet, MessageViewSet
from maalem.notifications.views import NotificationViewSet
from maalem.reviews.views import ReviewViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    path('users/login/client/', UserViewSet.as_view({'post': 'login_client'}), name='login-client'),
    path('users/login/artisan/', UserViewSet.as_view({'post': 'login_artisan'}), name='login-artisan'),
]
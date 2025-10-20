from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Post, Like, Comment, SavedPost, Share, View
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, SavedPostSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_parsers(self):
        """
        Use MultiPartParser and FormParser only for create/update actions
        Use JSONParser for other actions (like add_comment)
        """
        if hasattr(self, 'action') and self.action in ['create', 'update', 'partial_update']:
            return [MultiPartParser(), FormParser()]
        return [JSONParser(), MultiPartParser(), FormParser()]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )
        if not created:
            like.delete()
            return Response({'status': 'unliked'})
        return Response({'status': 'liked'})

    @action(detail=True, methods=['post'])
    def save_post(self, request, pk=None):
        post = self.get_object()
        saved, created = SavedPost.objects.get_or_create(
            user=request.user,
            post=post
        )
        if not created:
            saved.delete()
            return Response({'status': 'unsaved'})
        return Response({'status': 'saved'})

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        """Share a post and increment share count"""
        post = self.get_object()
        # Create a share record
        Share.objects.create(
            user=request.user if request.user.is_authenticated else None,
            post=post
        )
        return Response({
            'status': 'shared',
            'shares_count': post.shares.count()
        })

    @action(detail=True, methods=['post'])
    def view(self, request, pk=None):
        """Track post view"""
        post = self.get_object()
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Create view record if user is authenticated or track by IP
        if request.user.is_authenticated:
            View.objects.get_or_create(
                user=request.user,
                post=post
            )
        else:
            # For anonymous users, create view with IP
            View.objects.create(
                post=post,
                ip_address=ip
            )
        
        return Response({
            'status': 'viewed',
            'views_count': post.views.count()
        })

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(user=request.user, post=post)
            # Return comment with user data in the expected format
            return Response({
                'id': comment.id,
                'user': {
                    'id': comment.user.id,
                    'name': comment.user.username,
                    'avatar': comment.user.profile_picture.url if comment.user.profile_picture else '/placeholder-user.svg'
                },
                'content': comment.content,
                'created_at': comment.created_at.isoformat()
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def saved(self, request):
        saved_posts = SavedPost.objects.filter(user=request.user)
        serializer = SavedPostSerializer(saved_posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_artisan(self, request):
        artisan_id = request.query_params.get('artisan_id')
        if artisan_id:
            posts = self.queryset.filter(author_id=artisan_id)
            serializer = self.get_serializer(posts, many=True)
            return Response(serializer.data)
        return Response({'error': 'artisan_id is required'}, 
                      status=status.HTTP_400_BAD_REQUEST)
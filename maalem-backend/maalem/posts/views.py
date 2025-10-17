from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Post, Like, Comment, SavedPost
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, SavedPostSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

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
    def add_comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
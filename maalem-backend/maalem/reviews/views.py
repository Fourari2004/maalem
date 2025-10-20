from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Review
from .serializers import ReviewSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Review.objects.all()
        
        # Filter by artisan if provided
        artisan_id = self.request.query_params.get('artisan', None)
        if artisan_id:
            queryset = queryset.filter(artisan_id=artisan_id)
        
        return queryset.select_related('artisan', 'reviewer')
    
    def get_permissions(self):
        # Allow anyone to view reviews, but only authenticated users to create
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        # Check if user is a client
        if request.user.user_type != 'client':
            return Response({
                'error': 'Seuls les clients peuvent laisser des avis.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Update artisan's average rating
        artisan = serializer.instance.artisan
        self.update_artisan_rating(artisan)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Check if user is the reviewer
        if instance.reviewer != request.user:
            return Response({
                'error': 'Vous ne pouvez modifier que vos propres avis.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Update artisan's average rating
        self.update_artisan_rating(instance.artisan)
        
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Check if user is the reviewer
        if instance.reviewer != request.user:
            return Response({
                'error': 'Vous ne pouvez supprimer que vos propres avis.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        artisan = instance.artisan
        self.perform_destroy(instance)
        
        # Update artisan's average rating
        self.update_artisan_rating(artisan)
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update_artisan_rating(self, artisan):
        """Update artisan's average rating based on all their reviews"""
        reviews = Review.objects.filter(artisan=artisan)
        if reviews.exists():
            avg_rating = sum([r.rating for r in reviews]) / reviews.count()
            artisan.rating = round(avg_rating, 2)
            artisan.save(update_fields=['rating'])
        else:
            artisan.rating = 0.0
            artisan.save(update_fields=['rating'])
    
    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        """Get all reviews given by the current user"""
        reviews = Review.objects.filter(reviewer=request.user)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def can_review(self, request):
        """Check if the current user can review a specific artisan"""
        artisan_id = request.query_params.get('artisan_id')
        
        if not artisan_id:
            return Response({
                'error': 'artisan_id parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user is a client
        if request.user.user_type != 'client':
            return Response({
                'can_review': False,
                'reason': 'Only clients can leave reviews'
            })
        
        # Check if already reviewed
        has_reviewed = Review.objects.filter(
            artisan_id=artisan_id,
            reviewer=request.user
        ).exists()
        
        return Response({
            'can_review': not has_reviewed,
            'reason': 'Already reviewed' if has_reviewed else None
        })

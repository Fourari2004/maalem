from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth import get_user_model
from django.db.models import Q
from .serializers import UserSerializer, UserRegistrationSerializer, UserUpdateSerializer, FollowSerializer, ProfilePictureUploadSerializer
from .models import Follow, ProfilePictureUpload
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['login_client', 'login_artisan']:
            permission_classes = [AllowAny]
        elif self.action in ['artisans', 'list', 'retrieve']:
            # Allow anyone to view artisans and user profiles
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return UserUpdateSerializer
        elif self.action == 'upload_profile_picture':
            return ProfilePictureUploadSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login_client(self, request):
        """Login endpoint for client accounts"""
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Find client user with this email
        try:
            user = User.objects.get(email=email, user_type='client')
            if user.check_password(password):
                # Generate tokens
                refresh = RefreshToken.for_user(user)
                serializer = self.get_serializer(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': serializer.data
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'No client account found with this email'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login_artisan(self, request):
        """Login endpoint for artisan accounts"""
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Find artisan user with this email
        try:
            user = User.objects.get(email=email, user_type='artisan')
            if user.check_password(password):
                # Generate tokens
                refresh = RefreshToken.for_user(user)
                serializer = self.get_serializer(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': serializer.data
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'No artisan account found with this email'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'])
    def artisans(self, request):
        artisans = User.objects.filter(user_type='artisan')
        page = self.paginate_queryset(artisans)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(artisans, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'], url_path='update-profile')
    def update_me(self, request):
        # Allow users to update their own profile
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['patch'], url_path='update-location')
    def update_location(self, request):
        user = request.user
        user.latitude = request.data.get('latitude')
        user.longitude = request.data.get('longitude')
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        """Change user password"""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')
        
        # Validate input
        if not old_password or not new_password or not new_password_confirm:
            return Response(
                {'error': 'Tous les champs sont requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if new passwords match
        if new_password != new_password_confirm:
            return Response(
                {'error': 'Les nouveaux mots de passe ne correspondent pas'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify old password
        if not user.check_password(old_password):
            return Response(
                {'error': 'Le mot de passe actuel est incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check password strength (minimum 8 characters)
        if len(new_password) < 8:
            return Response(
                {'error': 'Le nouveau mot de passe doit contenir au moins 8 caractères'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        return Response(
        {'message': 'Mot de passe changé avec succès'},
        status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'], url_path='upload-profile-picture', parser_classes=[MultiPartParser, FormParser])
    def upload_profile_picture(self, request):
        """Upload a profile picture with confirmation workflow"""
        if not request.FILES.get('image'):
            return Response(
                {'error': 'Aucune image fournie'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create a profile picture upload record
        serializer = ProfilePictureUploadSerializer(
            data={'image': request.FILES['image']},
            context={'request': request}
        )
        
        if serializer.is_valid():
            # Save the upload record
            upload_record = serializer.save()
            
            # Return the upload record details
            return Response({
                'message': 'Image téléchargée avec succès. En attente de confirmation.',
                'upload': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'], url_path='confirm-profile-picture')
    def confirm_profile_picture(self, request):
        """Confirm a profile picture upload and apply it to the user's profile"""
        upload_id = request.data.get('upload_id')
        
        if not upload_id:
            return Response(
                {'error': 'ID de téléchargement requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Get the upload record
            upload_record = ProfilePictureUpload.objects.get(
                id=upload_id,
                user=request.user,
                is_confirmed=False
            )
            
            # Confirm the upload
            upload_record.is_confirmed = True
            upload_record.save()
            
            # Update the user's profile picture
            request.user.profile_picture = upload_record.image
            request.user.save(update_fields=['profile_picture'])
            
            # Return updated user data
            user_serializer = self.get_serializer(request.user)
            return Response({
                'message': 'Image de profil confirmée et appliquée avec succès',
                'user': user_serializer.data
            }, status=status.HTTP_200_OK)
            
        except ProfilePictureUpload.DoesNotExist:
            return Response(
                {'error': 'Enregistrement de téléchargement non trouvé ou déjà confirmé'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        """
        Follow/Unfollow a user (toggle).
        Similar to Instagram's follow button.
        POST /api/users/{id}/follow/
        """
        user_to_follow = self.get_object()
        current_user = request.user
        
        # Check if user is trying to follow themselves
        if current_user == user_to_follow:
            return Response(
                {'error': 'Vous ne pouvez pas vous suivre vous-même'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already following
        follow_instance = Follow.objects.filter(
            follower=current_user,
            followed=user_to_follow
        ).first()
        
        if follow_instance:
            # Unfollow (like clicking "Abonné" to unsubscribe)
            follow_instance.delete()
            
            return Response({
                'status': 'unfollowed',
                'message': f'Vous ne suivez plus {user_to_follow.get_full_name() or user_to_follow.username}',
                'is_following': False,
                'followers_count': user_to_follow.followers.count()
            })
        else:
            # Follow (like clicking "Suivre")
            follow_instance = Follow.objects.create(
                follower=current_user,
                followed=user_to_follow
            )
            
            # Create notification for the followed user
            try:
                from maalem.notifications.models import Notification
                Notification.objects.create(
                    user=user_to_follow,
                    sender=current_user,
                    notification_type='follow',
                    text=f"{current_user.get_full_name() or current_user.username} vous suit maintenant"
                )
            except Exception as e:
                # If notification fails, still return success
                print(f"Failed to create notification: {e}")
            
            return Response({
                'status': 'followed',
                'message': f'Vous suivez maintenant {user_to_follow.get_full_name() or user_to_follow.username}',
                'is_following': True,
                'followers_count': user_to_follow.followers.count()
            })
    
    @action(detail=True, methods=['get'], url_path='followers')
    def get_followers(self, request, pk=None):
        """
        Get list of users following this user.
        GET /api/users/{id}/followers/
        """
        user = self.get_object()
        followers = Follow.objects.filter(followed=user).select_related('follower')
        serializer = FollowSerializer(followers, many=True)
        return Response({
            'count': followers.count(),
            'followers': serializer.data
        })
    
    @action(detail=True, methods=['get'], url_path='following')
    def get_following(self, request, pk=None):
        """
        Get list of users this user is following.
        GET /api/users/{id}/following/
        """
        user = self.get_object()
        following = Follow.objects.filter(follower=user).select_related('followed')
        serializer = FollowSerializer(following, many=True)
        return Response({
            'count': following.count(),
            'following': serializer.data
        })
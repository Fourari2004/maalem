from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('artisan', 'Artisan'),
    )
    
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='client'
    )
    
    # Verification field to mark verified accounts
    is_verified = models.BooleanField(
        default=False,
        help_text='Designates whether this user account has been verified by admin.'
    )
    
    # Contact and profile fields
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    bio = models.TextField(blank=True)
    
    # Champs spécifiques pour les artisans
    specialty = models.CharField(max_length=100, blank=True)
    experience_years = models.PositiveIntegerField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Allow same email for different user types by adding a custom constraint
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        # Add unique constraint for email + user_type combination
        unique_together = ('email', 'user_type')
        
    def save(self, *args, **kwargs):
        # Custom save logic to ensure uniqueness of email+user_type combination
        if not self.username:
            # Generate username based on email and user_type
            base_username = self.email.split('@')[0]
            user_type_suffix = self.user_type[0]  # 'c' for client, 'a' for artisan
            self.username = f"{base_username}_{user_type_suffix}"
            
            # Ensure username is unique
            counter = 1
            original_username = self.username
            while User.objects.filter(username=self.username).exists():
                self.username = f"{original_username}_{counter}"
                counter += 1
                
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
class ProfilePictureUpload(models.Model):
    """
    Model to track profile picture uploads with confirmation status.
    This provides a confirmation table for profile photo uploads.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='profile_picture_uploads',
        help_text='The user who uploaded the profile picture'
    )
    
    # Store the image file
    image = models.ImageField(
        upload_to='profile_pictures/confirmations/',
        help_text='The uploaded profile picture'
    )
    
    # Confirmation status
    is_confirmed = models.BooleanField(
        default=False,
        help_text='Whether the profile picture has been confirmed and applied'
    )
    
    # Upload metadata
    uploaded_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    
    # Original filename
    original_filename = models.CharField(max_length=255, blank=True)
    
    class Meta:
        verbose_name = 'Profile Picture Upload'
        verbose_name_plural = 'Profile Picture Uploads'
        ordering = ['-uploaded_at']
        
    def __str__(self):
        return f"Profile picture for {self.user.get_full_name()} ({'confirmed' if self.is_confirmed else 'pending'})"
    
    def save(self, *args, **kwargs):
        # If this is a confirmed upload, update the user's profile picture
        if self.is_confirmed and self.image:
            self.user.profile_picture = self.image
            self.user.save(update_fields=['profile_picture'])
            # Set confirmed timestamp
            if not self.confirmed_at:
                self.confirmed_at = timezone.now()
        super().save(*args, **kwargs)


class Follow(models.Model):
    """
    Model to represent follow relationships between users.
    Similar to Instagram's followers table.
    """
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',  # Users this user is following
        help_text='The user who is following'
    )
    followed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',  # Users following this user
        help_text='The user being followed'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'followed')
        ordering = ['-created_at']
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
        indexes = [
            models.Index(fields=['follower', 'followed']),
            models.Index(fields=['followed', 'follower']),
        ]
    
    def __str__(self):
        return f"{self.follower.get_full_name()} follows {self.followed.get_full_name()}"
    
    def save(self, *args, **kwargs):
        # Prevent users from following themselves
        if self.follower == self.followed:
            raise ValueError("Users cannot follow themselves")
        super().save(*args, **kwargs)
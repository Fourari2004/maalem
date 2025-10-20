from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Follow


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User admin with is_verified field management
    """
    list_display = ['email', 'first_name', 'last_name', 'user_type', 'is_verified', 'is_staff', 'date_joined']
    list_filter = ['user_type', 'is_verified', 'is_staff', 'is_superuser', 'is_active']
    search_fields = ['email', 'first_name', 'last_name', 'username']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number', 'bio')}),
        (_('User Type'), {'fields': ('user_type', 'is_verified')}),
        (_('Artisan Info'), {
            'fields': ('specialty', 'experience_years', 'rating', 'address', 'latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Profile'), {'fields': ('profile_picture',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'user_type', 'password1', 'password2'),
        }),
    )
    
    # Actions to quickly verify/unverify users
    actions = ['verify_users', 'unverify_users']
    
    def verify_users(self, request, queryset):
        """Mark selected users as verified"""
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} utilisateur(s) marqué(s) comme vérifié(s).')
    verify_users.short_description = "Marquer comme vérifié"
    
    def unverify_users(self, request, queryset):
        """Mark selected users as unverified"""
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} utilisateur(s) marqué(s) comme non vérifié(s).')
    unverify_users.short_description = "Marquer comme non vérifié"


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """
    Admin interface for Follow relationships
    """
    list_display = ['follower', 'followed', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__email', 'follower__first_name', 'follower__last_name',
                    'followed__email', 'followed__first_name', 'followed__last_name']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('follower', 'followed')

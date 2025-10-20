from django.contrib import admin
from .models import Post, Like, Comment, SavedPost, Share, View

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'description', 'author__username']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'created_at']
    list_filter = ['created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'user__username']

@admin.register(SavedPost)
class SavedPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'saved_at']
    list_filter = ['saved_at']

@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'created_at']
    list_filter = ['created_at']

@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'ip_address', 'created_at']
    list_filter = ['created_at']

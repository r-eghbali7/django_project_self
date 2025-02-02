from django.contrib import admin
from .models import Post, Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
    
@admin.register(Post)    
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'created_date', 'status']
    list_filter = ['status', 'created_date', 'update_date']
    search_fields = ['title', 'text']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'created_date'
    ordering = ['status', 'created_date']


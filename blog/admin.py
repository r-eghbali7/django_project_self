from django.contrib import admin
from .models import Category,Post, Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
    
@admin.register(Post)    
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'created_date', 'status','tag_list']
    list_filter = ['status', 'created_date', 'update_date']
    search_fields = ['title', 'text']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'created_date'
    ordering = ['status', 'created_date']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
    
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    
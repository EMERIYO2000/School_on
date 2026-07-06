from django.contrib import admin
from .models import ForumPost, ForumThread
# Register your models here.

@admin.register(ForumThread)
class ForumThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'is_closed')
    list_filter = ('category', 'created_at', 'is_closed')
    search_fields = ('title', 'author__username', 'category__name')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    
    
@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('thread', 'author', 'created_at', 'is_accepted_solution')
    list_filter = ('created_at', 'is_accepted_solution')
    search_fields = ('thread__title', 'author__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
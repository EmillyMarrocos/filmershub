from django.contrib import admin
from .models import Post, Like, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_type', 'content_preview', 'likes_count', 'comments_count', 'created_at')
    list_filter = ('post_type', 'created_at')
    search_fields = ('author__email', 'content')
    raw_id_fields = ('author',)

    def content_preview(self, obj):
        return obj.content[:80] + '...' if len(obj.content) > 80 else obj.content
    content_preview.short_description = 'Conteúdo'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    raw_id_fields = ('user', 'post')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content_preview', 'created_at')
    search_fields = ('author__email', 'content')
    raw_id_fields = ('author', 'post', 'parent')

    def content_preview(self, obj):
        return obj.content[:60] + '...' if len(obj.content) > 60 else obj.content
    content_preview.short_description = 'Conteúdo'

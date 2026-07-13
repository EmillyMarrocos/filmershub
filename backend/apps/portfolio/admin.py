from django.contrib import admin
from .models import Category, Work, WorkMedia, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'videomaker', 'work_type', 'category', 'status', 'created_at')
    list_filter = ('status', 'work_type', 'category')
    search_fields = ('title', 'videomaker__email')
    raw_id_fields = ('videomaker',)


@admin.register(WorkMedia)
class WorkMediaAdmin(admin.ModelAdmin):
    list_display = ('work', 'media_type', 'order')
    list_filter = ('media_type',)
    raw_id_fields = ('work',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'videomaker', 'rating', 'created_at')
    list_filter = ('rating',)
    raw_id_fields = ('reviewer', 'videomaker', 'work')

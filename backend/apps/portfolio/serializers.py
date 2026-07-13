# ===========================================
# FILMERSHUB - PORTFOLIO SERIALIZERS
# ===========================================

from rest_framework import serializers
from .models import Category, Work, WorkMedia, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon']


class WorkMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkMedia
        fields = ['id', 'file', 'media_type', 'caption', 'order']


class WorkListSerializer(serializers.ModelSerializer):
    videomaker_name = serializers.CharField(source='videomaker.full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True, default=None)
    is_mine = serializers.SerializerMethodField()

    class Meta:
        model = Work
        fields = [
            'id', 'title', 'description', 'work_type', 'category_name',
            'thumbnail', 'external_url', 'videomaker_name', 'videomaker',
            'views_count', 'likes_count', 'status', 'published_at',
            'client_name', 'location', 'equipment_used', 'is_mine',
        ]

    def get_is_mine(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.videomaker_id == request.user.id
        return False


class WorkDetailSerializer(serializers.ModelSerializer):
    videomaker_name = serializers.CharField(source='videomaker.full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True, default=None)
    media = WorkMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Work
        fields = [
            'id', 'title', 'description', 'work_type',
            'category', 'category_name', 'file', 'thumbnail',
            'external_url', 'client_name', 'location',
            'equipment_used', 'views_count', 'likes_count',
            'videomaker_name', 'media', 'status', 'published_at', 'created_at',
        ]


class WorkCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = [
            'title', 'description', 'work_type', 'category',
            'file', 'thumbnail', 'external_url',
            'client_name', 'location', 'equipment_used', 'status',
        ]


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.full_name', read_only=True)
    videomaker_name = serializers.CharField(source='videomaker.full_name', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'reviewer', 'reviewer_name', 'videomaker',
            'videomaker_name', 'work', 'rating', 'comment',
            'response', 'responded_at', 'created_at',
        ]
        read_only_fields = ['reviewer', 'response', 'responded_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['videomaker', 'work', 'rating', 'comment']

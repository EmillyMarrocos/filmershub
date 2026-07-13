# ===========================================
# FILMERSHUB - FEED SERIALIZERS
# ===========================================

from rest_framework import serializers
from .models import Post, Like, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_name', 'content', 'replies', 'likes_count', 'created_at']
        read_only_fields = ['author', 'likes_count']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []


class PostListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    author_avatar = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_name', 'author_avatar',
            'content', 'post_type', 'media', 'link_url',
            'link_title', 'link_description',
            'likes_count', 'comments_count', 'shares_count',
            'is_liked', 'created_at',
        ]

    def get_author_avatar(self, obj):
        if obj.author.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.author.avatar.url)
        return None

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, post=obj).exists()
        return False


class PostDetailSerializer(PostListSerializer):
    comments = serializers.SerializerMethodField()

    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ['description', 'updated_at', 'comments']

    def get_comments(self, obj):
        comments = obj.comments.filter(parent=None)
        return CommentSerializer(comments, many=True).data


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content', 'post_type', 'media', 'link_url', 'link_title', 'link_description']


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['user']


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['parent', 'content']
        read_only_fields = ['author', 'post']

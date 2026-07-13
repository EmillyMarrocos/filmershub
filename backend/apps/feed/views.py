# ===========================================
# FILMERSHUB - FEED VIEWS
# ===========================================

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Post, Like, Comment
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostCreateSerializer,
    PostUpdateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
)


class PostListView(generics.ListAPIView):
    """GET /api/v1/feed/"""
    serializer_class = PostListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Post.objects.all()


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/v1/feed/<uuid:pk>/"""
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return PostUpdateSerializer
        return PostDetailSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Você só pode editar seus próprios posts.')
        partial = request.method == 'PATCH'
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.refresh_from_db()
        return Response(PostDetailSerializer(instance, context={'request': request}).data)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Você só pode excluir seus próprios posts.')
        instance.delete()


class PostCreateView(generics.CreateAPIView):
    """POST /api/v1/feed/"""
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikeToggleView(APIView):
    """POST /api/v1/feed/<uuid:post_id>/like/"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()
            post.likes_count = max(0, post.likes_count - 1)
            post.save(update_fields=['likes_count'])
            return Response({'detail': 'Curtida removida.'}, status=status.HTTP_200_OK)

        post.likes_count += 1
        post.save(update_fields=['likes_count'])
        return Response({'detail': 'Post curtido!'}, status=status.HTTP_201_CREATED)


class CommentCreateView(generics.CreateAPIView):
    """POST /api/v1/feed/<uuid:post_id>/comments/"""
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        comment = serializer.save(author=self.request.user, post=post)
        post.comments_count += 1
        post.save(update_fields=['comments_count'])


class CommentListView(generics.ListAPIView):
    """GET /api/v1/feed/<uuid:post_id>/comments/"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Comment.objects.filter(
            post_id=self.kwargs['post_id'],
            parent=None
        )


class SharePostView(APIView):
    """POST /api/v1/feed/<uuid:post_id>/share/"""
    permission_classes = [permissions.AllowAny]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.shares_count += 1
        post.save(update_fields=['shares_count'])
        return Response(
            {'shares_count': post.shares_count},
            status=status.HTTP_200_OK
        )

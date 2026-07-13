# ===========================================
# FILMERSHUB - PORTFOLIO VIEWS
# ===========================================

from rest_framework import generics, permissions, filters
from django.shortcuts import get_object_or_404
from .models import Category, Work, Review
from .serializers import (
    CategorySerializer,
    WorkListSerializer,
    WorkDetailSerializer,
    WorkCreateUpdateSerializer,
    ReviewSerializer,
    ReviewCreateSerializer,
)


class CategoryListView(generics.ListAPIView):
    """GET /api/v1/portfolio/categories/"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class WorkListView(generics.ListCreateAPIView):
    """GET / POST /api/v1/portfolio/works/"""
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'client_name']
    ordering_fields = ['created_at', 'views_count', 'likes_count']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WorkCreateUpdateSerializer
        return WorkListSerializer

    def get_queryset(self):
        qs = Work.objects.filter(status='published')
        videomaker_id = self.request.query_params.get('videomaker')
        if videomaker_id:
            qs = qs.filter(videomaker_id=videomaker_id)
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category__slug=category)
        return qs

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(videomaker=self.request.user)


class WorkDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH/DELETE /api/v1/portfolio/works/<uuid:pk>/"""
    queryset = Work.objects.all()
    serializer_class = WorkDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return WorkCreateUpdateSerializer
        return WorkDetailSerializer

    def perform_update(self, serializer):
        if serializer.instance.videomaker != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Você só pode editar seus próprios trabalhos.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.videomaker != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Você só pode excluir seus próprios trabalhos.')
        instance.delete()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        return super().retrieve(request, *args, **kwargs)


class WorkCreateView(generics.CreateAPIView):
    """POST /api/v1/portfolio/works/"""
    serializer_class = WorkCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(videomaker=self.request.user)


class WorkUpdateView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH/DELETE /api/v1/portfolio/works/<uuid:pk>/mine/"""
    serializer_class = WorkCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Work.objects.filter(videomaker=self.request.user)


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/portfolio/reviews/?videomaker=<uuid> — listar reviews
    POST /api/v1/portfolio/reviews/                  — criar review
    """
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewSerializer

    def get_queryset(self):
        qs = Review.objects.all()
        videomaker_id = self.request.query_params.get('videomaker')
        if videomaker_id:
            qs = qs.filter(videomaker_id=videomaker_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


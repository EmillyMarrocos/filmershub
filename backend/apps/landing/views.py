# ===========================================
# FILMERSHUB - LANDING PAGE VIEWS
# ===========================================

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth import get_user_model
from apps.portfolio.models import Work
from apps.feed.models import Post

User = get_user_model()


class LandingStatsView(APIView):
    """GET /api/v1/landing/stats/"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            'videomakers': User.objects.filter(is_videomaker=True, is_active=True).count(),
            'works': Work.objects.filter(status='published').count(),
            'posts': Post.objects.count(),
            'clients': User.objects.filter(is_client=True, is_active=True).count(),
        })


class FeaturedVideomakersView(APIView):
    """GET /api/v1/landing/featured-videomakers/"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        from apps.accounts.serializers import UserListSerializer
        users = User.objects.filter(
            is_videomaker=True,
            is_active=True,
        ).order_by('-date_joined')[:6]
        return Response(UserListSerializer(users, many=True, context={'request': request}).data)


class FeaturedWorksView(APIView):
    """GET /api/v1/landing/featured-works/"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        from apps.portfolio.serializers import WorkListSerializer
        works = Work.objects.filter(
            status='published'
        ).select_related('videomaker').order_by('-views_count')[:8]
        return Response(WorkListSerializer(works, many=True, context={'request': request}).data)

# ===========================================
# FILMERSHUB - NOTIFICATIONS VIEWS
# ===========================================

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer, NotificationListSerializer


class NotificationListView(generics.ListAPIView):
    """GET /api/v1/notifications/"""
    serializer_class = NotificationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)


class NotificationDetailView(generics.RetrieveAPIView):
    """GET /api/v1/notifications/<uuid:pk>/"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)


class NotificationMarkReadView(APIView):
    """POST /api/v1/notifications/<uuid:pk>/read/"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        notification = Notification.objects.get(
            id=pk,
            recipient=request.user
        )
        notification.mark_as_read()
        return Response({'detail': 'Notificação marcada como lida.'})


class NotificationMarkAllReadView(APIView):
    """POST /api/v1/notifications/read-all/"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        from django.utils import timezone
        Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True, read_at=timezone.now())
        return Response({'detail': 'Todas as notificações marcadas como lidas.'})


class NotificationUnreadCountView(APIView):
    """GET /api/v1/notifications/unread-count/"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
        return Response({'unread_count': count})

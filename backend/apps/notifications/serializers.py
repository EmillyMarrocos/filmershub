# ===========================================
# FILMERSHUB - NOTIFICATIONS SERIALIZERS
# ===========================================

from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.full_name', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'sender', 'sender_name', 'notification_type',
            'title', 'message', 'link', 'extra_data',
            'is_read', 'read_at', 'created_at',
        ]
        read_only_fields = ['is_read', 'read_at']


class NotificationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'title', 'message',
            'link', 'is_read', 'created_at',
        ]

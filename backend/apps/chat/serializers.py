# ===========================================
# FILMERSHUB - CHAT SERIALIZERS
# ===========================================

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message

User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.full_name', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'sender_name', 'message_type',
            'content', 'file', 'image', 'is_read', 'created_at',
        ]
        read_only_fields = ['sender', 'is_read']


class ChatRoomListSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    last_message_content = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = [
            'id', 'room_type', 'other_user',
            'last_message_content', 'unread_count', 'updated_at',
        ]

    def get_other_user(self, obj):
        request = self.context.get('request')
        if request:
            other = obj.participants.exclude(id=request.user.id).first()
            if other:
                return {
                    'id': str(other.id),
                    'name': other.full_name,
                    'avatar': other.avatar.url if other.avatar else None,
                }
        return None

    def get_last_message_content(self, obj):
        if obj.last_message:
            return obj.last_message.content[:100]
        return None

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0


class ChatRoomDetailSerializer(serializers.ModelSerializer):
    participants_data = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'room_type', 'participants_data', 'messages', 'created_at']

    def get_participants_data(self, obj):
        return [
            {
                'id': str(p.id),
                'name': p.full_name,
                'avatar': p.avatar.url if p.avatar else None,
            }
            for p in obj.participants.all()
        ]

    def get_messages(self, obj):
        messages = obj.messages.all()[:50]
        return MessageSerializer(messages, many=True).data

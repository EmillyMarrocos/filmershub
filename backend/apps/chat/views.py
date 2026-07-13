# ===========================================
# FILMERSHUB - CHAT VIEWS
# ===========================================

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import ChatRoom, Message
from .serializers import (
    ChatRoomListSerializer,
    ChatRoomDetailSerializer,
    MessageSerializer,
)

User = get_user_model()


class ChatRoomListView(generics.ListAPIView):
    """GET /api/v1/chat/rooms/"""
    serializer_class = ChatRoomListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatRoom.objects.filter(
            participants=self.request.user
        ).order_by('-updated_at')


class ChatRoomCreateView(APIView):
    """POST /api/v1/chat/rooms/"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(
                {'detail': 'user_id é obrigatório.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        other_user = get_object_or_404(User, id=user_id)

        if other_user == request.user:
            return Response(
                {'detail': 'Não pode criar sala consigo mesmo.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verifica se já existe sala entre os dois
        existing = ChatRoom.objects.filter(
            participants=request.user
        ).filter(
            participants=other_user
        ).first()

        if existing:
            serializer = ChatRoomDetailSerializer(existing, context={'request': request})
            return Response(serializer.data)

        # Cria nova sala
        room = ChatRoom.objects.create(room_type='direct')
        room.participants.add(request.user, other_user)

        serializer = ChatRoomDetailSerializer(room, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChatRoomDetailView(generics.RetrieveAPIView):
    """GET /api/v1/chat/rooms/<uuid:pk>/"""
    serializer_class = ChatRoomDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatRoom.objects.filter(participants=self.request.user)


class MessageListView(generics.ListAPIView):
    """GET /api/v1/chat/rooms/<uuid:room_id>/messages/"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            room_id=self.kwargs['room_id']
        ).order_by('-created_at')[:50]


class MessageCreateView(APIView):
    """POST /api/v1/chat/rooms/<uuid:room_id>/messages/"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, room_id):
        room = get_object_or_404(
            ChatRoom.objects.filter(participants=request.user),
            id=room_id
        )

        content = request.data.get('content', '')
        message_type = request.data.get('message_type', 'text')

        message = Message.objects.create(
            room=room,
            sender=request.user,
            content=content,
            message_type=message_type,
        )

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MarkMessagesReadView(APIView):
    """POST /api/v1/chat/rooms/<uuid:room_id>/read/"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, room_id):
        room = get_object_or_404(
            ChatRoom.objects.filter(participants=request.user),
            id=room_id
        )

        updated = Message.objects.filter(
            room=room,
            is_read=False
        ).exclude(sender=request.user).update(is_read=True)

        return Response({'marked_read': updated})

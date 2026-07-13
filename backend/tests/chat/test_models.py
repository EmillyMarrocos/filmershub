# ===========================================
# FILMERSHUB - TESTES DE MODELOS (CHAT)
# ===========================================

import pytest
from django.contrib.auth import get_user_model
from apps.chat.models import ChatRoom, Message

User = get_user_model()


@pytest.mark.django_db
class TestChatRoom:
    """Testes para o modelo ChatRoom."""

    def test_create_room(self, user, videomaker_user):
        """Testa criação de sala de chat."""
        room = ChatRoom.objects.create(room_type='direct')
        room.participants.add(user, videomaker_user)
        assert room.participants.count() == 2

    def test_room_str(self, user, videomaker_user):
        """Testa representação string."""
        room = ChatRoom.objects.create(room_type='direct')
        room.participants.add(user, videomaker_user)
        assert str(room) != ''


@pytest.mark.django_db
class TestMessage:
    """Testes para o modelo Message."""

    def test_create_message(self, user):
        """Testa criação de mensagem."""
        room = ChatRoom.objects.create(room_type='direct')
        room.participants.add(user)
        message = Message.objects.create(
            room=room,
            sender=user,
            content='Olá!',
        )
        assert message.content == 'Olá!'

    def test_message_str(self, user):
        """Testa representação string."""
        room = ChatRoom.objects.create(room_type='direct')
        room.participants.add(user)
        message = Message(
            room=room,
            sender=user,
            content='Teste',
        )
        assert str(message) != ''

    def test_message_updates_room(self, user):
        """Testa que mensagem atualiza última mensagem da sala."""
        room = ChatRoom.objects.create(room_type='direct')
        room.participants.add(user)
        message = Message.objects.create(
            room=room,
            sender=user,
            content='Primeira mensagem',
        )
        room.refresh_from_db()
        assert room.last_message == message

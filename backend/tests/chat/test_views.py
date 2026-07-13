# ===========================================
# FILMERSHUB - TESTES DE VIEWS (CHAT API)
# ===========================================

import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.chat.models import ChatRoom, Message

User = get_user_model()


@pytest.mark.django_db
class TestChatRoomListView:
    """Testes para listagem de salas."""

    def test_list_rooms(self, authenticated_client, user):
        """Testa listagem de salas."""
        room = ChatRoom.objects.create(room_type='direct')
        room.participants.add(user)
        url = reverse('room-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestChatRoomCreateView:
    """Testes para criação de sala."""

    def test_create_room(self, authenticated_client, user, videomaker_user):
        """Testa criação de sala com outro usuário."""
        url = reverse('room-create')
        data = {'user_id': str(videomaker_user.id)}
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_room_with_self(self, authenticated_client, user):
        """Testa que não pode criar sala consigo mesmo."""
        url = reverse('room-create')
        data = {'user_id': str(user.id)}
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_room_existing(self, authenticated_client, user, videomaker_user):
        """Testa que retorna sala existente."""
        room = ChatRoom.objects.create(room_type='direct')
        room.participants.add(user, videomaker_user)

        url = reverse('room-create')
        data = {'user_id': str(videomaker_user.id)}
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestMessageCreateView:
    """Testes para envio de mensagem."""

    def test_send_message(self, authenticated_client, user):
        """Testa envio de mensagem."""
        room = ChatRoom.objects.create(room_type='direct')
        room.participants.add(user)
        url = reverse('message-create', kwargs={'room_id': room.id})
        data = {'content': 'Olá!', 'message_type': 'text'}
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Message.objects.filter(room=room).count() == 1

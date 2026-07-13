# ===========================================
# FILMERSHUB - TESTES DE MODELOS (NOTIFICATIONS)
# ===========================================

import pytest
from django.contrib.auth import get_user_model
from apps.notifications.models import Notification

User = get_user_model()


@pytest.mark.django_db
class TestNotification:
    """Testes para o modelo Notification."""

    def test_create_notification(self, user):
        """Testa criação de notificação."""
        notification = Notification.objects.create(
            recipient=user,
            notification_type='message',
            title='Nova mensagem',
            message='Você recebeu uma nova mensagem.',
        )
        assert notification.title == 'Nova mensagem'
        assert notification.is_read is False

    def test_notification_str(self, user):
        """Testa representação string."""
        notification = Notification(
            recipient=user,
            title='Teste',
        )
        assert str(notification) != ''

    def test_mark_as_read(self, user):
        """Testa marcação como lida."""
        notification = Notification.objects.create(
            recipient=user,
            notification_type='system',
            title='Sistema',
            message='Mensagem do sistema',
        )
        notification.mark_as_read()
        notification.refresh_from_db()
        assert notification.is_read is True
        assert notification.read_at is not None

    def test_notification_with_sender(self, user, videomaker_user):
        """Testa notificação com remetente."""
        notification = Notification.objects.create(
            recipient=user,
            sender=videomaker_user,
            notification_type='follow',
            title='Novo seguidor',
            message='John Doe começou a seguir você.',
        )
        assert notification.sender == videomaker_user

# ===========================================
# FILMERSHUB - MODELOS DE CHAT
# ===========================================
# Salas de chat e mensagens em tempo real

from django.db import models
from django.conf import settings
import uuid


class ChatRoom(models.Model):
    """
    Sala de chat entre dois usuários.
    Criada automaticamente quando um usuário inicia uma conversa.
    """

    TYPE_CHOICES = [
        ('direct', 'Direto'),
        ('group', 'Grupo'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    room_type = models.CharField(
        'Tipo',
        max_length=10,
        choices=TYPE_CHOICES,
        default='direct'
    )

    # Participantes
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='chat_rooms',
        verbose_name='Participantes'
    )

    # Mensagem mais recente (para ordenação)
    last_message = models.ForeignKey(
        'Message',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name='Última Mensagem'
    )

    # Timestamps
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Sala de Chat'
        verbose_name_plural = 'Salas de Chat'
        ordering = ['-updated_at']

    def __str__(self):
        participants = self.participants.all()
        return ' - '.join([p.full_name for p in participants[:2]])


class Message(models.Model):
    """
    Mensagem em uma sala de chat.
    Suporta texto, imagens e arquivos.
    """

    TYPE_CHOICES = [
        ('text', 'Texto'),
        ('image', 'Imagem'),
        ('file', 'Arquivo'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Sala'
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='Remetente'
    )

    message_type = models.CharField(
        'Tipo',
        max_length=10,
        choices=TYPE_CHOICES,
        default='text'
    )

    content = models.TextField('Conteúdo', max_length=5000, blank=True)

    # Arquivo (opcional)
    file = models.FileField(
        'Arquivo',
        upload_to='chat/files/',
        blank=True,
        null=True
    )

    # Imagem (opcional)
    image = models.ImageField(
        'Imagem',
        upload_to='chat/images/',
        blank=True,
        null=True
    )

    # Status da mensagem
    is_read = models.BooleanField('Lida', default=False)

    # Timestamps
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender.full_name} em {self.room}'

    def save(self, *args, **kwargs):
        """Atualiza a última mensagem da sala ao enviar."""
        super().save(*args, **kwargs)
        self.room.last_message = self
        self.room.save()

# ===========================================
# FILMERSHUB - MODELOS DE NOTIFICAÇÕES
# ===========================================
# Notificações in-app e envio de email

from django.db import models
from django.conf import settings
import uuid


class Notification(models.Model):
    """
    Notificação in-app.
    Enviada quando algo importante acontece (mensagem, agendamento, pagamento, etc.)
    """

    TYPE_CHOICES = [
        ('message', 'Nova Mensagem'),
        ('booking_request', 'Solicitação de Agendamento'),
        ('booking_accepted', 'Agendamento Aceito'),
        ('booking_declined', 'Agendamento Recusado'),
        ('contract', 'Novo Contrato'),
        ('contract_signed', 'Contrato Assinado'),
        ('payment_received', 'Pagamento Recebido'),
        ('payment_failed', 'Pagamento Falhou'),
        ('review', 'Nova Avaliação'),
        ('follow', 'Novo Seguidor'),
        ('system', 'Sistema'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Destinatário'
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications_sent',
        verbose_name='Remetente'
    )

    notification_type = models.CharField(
        'Tipo',
        max_length=20,
        choices=TYPE_CHOICES,
        default='system'
    )

    title = models.CharField('Título', max_length=200)
    message = models.TextField('Mensagem', max_length=1000)

    # Dados extras (JSON)
    extra_data = models.JSONField(
        'Dados Extras',
        default=dict,
        blank=True
    )

    # Link para redirecionamento
    link = models.CharField('Link', max_length=500, blank=True)

    # Status
    is_read = models.BooleanField('Lida', default=False)
    read_at = models.DateTimeField('Lida em', null=True, blank=True)

    # Email
    email_sent = models.BooleanField('Email Enviado', default=False)
    email_sent_at = models.DateTimeField('Email Enviado em', null=True, blank=True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['notification_type']),
        ]

    def __str__(self):
        return f'{self.title} → {self.recipient.full_name}'

    def mark_as_read(self):
        """Marca a notificação como lida."""
        from django.utils import timezone
        self.is_read = True
        self.read_at = timezone.now()
        self.save(update_fields=['is_read', 'read_at'])

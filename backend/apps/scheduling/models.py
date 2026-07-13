# ===========================================
# FILMERSHUB - MODELOS DE AGENDAMENTO
# ===========================================
# Eventos, disponibilidade e solicitações

from django.db import models
from django.conf import settings
import uuid


class Availability(models.Model):
    """
    Disponibilidade semanal de um videomaker.
    Define os horários em que o videomaker está disponível.
    """

    DAY_CHOICES = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    videomaker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='availabilities',
        verbose_name='Videomaker'
    )

    day_of_week = models.IntegerField(
        'Dia da Semana',
        choices=DAY_CHOICES
    )

    start_time = models.TimeField('Horário Início')
    end_time = models.TimeField('Horário Fim')

    is_available = models.BooleanField('Disponível', default=True)

    class Meta:
        verbose_name = 'Disponibilidade'
        verbose_name_plural = 'Disponibilidades'
        unique_together = ('videomaker', 'day_of_week')
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f'{self.videomaker.full_name} - {self.get_day_of_week_display()}'


class Event(models.Model):
    """
    Evento agendado entre cliente e videomaker.
    Pode ser: ensaio, gravação, edição, etc.
    """

    TYPE_CHOICES = [
        ('wedding', 'Casamento'),
        ('corporate', 'Corporativo'),
        ('event', 'Evento'),
        ('shoot', 'Gravação'),
        ('editing', 'Edição'),
        ('meeting', 'Reunião'),
        ('other', 'Outro'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('confirmed', 'Confirmado'),
        ('in_progress', 'Em Andamento'),
        ('completed', 'Concluído'),
        ('cancelled', 'Cancelado'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição', max_length=2000, blank=True)

    event_type = models.CharField(
        'Tipo',
        max_length=20,
        choices=TYPE_CHOICES,
        default='other'
    )

    # Participantes
    videomaker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='videomaker_events',
        verbose_name='Videomaker'
    )

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_events',
        verbose_name='Cliente'
    )

    # Data e hora
    start_datetime = models.DateTimeField('Data/Hora Início')
    end_datetime = models.DateTimeField('Data/Hora Fim')

    # Localização
    location = models.CharField('Local', max_length=200, blank=True)
    address = models.TextField('Endereço', blank=True)

    # Valor
    total_price = models.DecimalField(
        'Valor Total',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Status
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # Notas
    notes = models.TextField('Observações', blank=True)

    # Timestamps
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['start_datetime']

    def __str__(self):
        return f'{self.title} - {self.start_datetime}'


class BookingRequest(models.Model):
    """
    Solicitação de agendamento enviada pelo cliente.
    O videomaker pode aceitar ou recusar.
    """

    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('accepted', 'Aceita'),
        ('declined', 'Recusada'),
        ('expired', 'Expirada'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='booking_requests_sent',
        verbose_name='Cliente'
    )

    videomaker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='booking_requests_received',
        verbose_name='Videomaker'
    )

    # Detalhes da solicitação
    event_type = models.CharField('Tipo de Evento', max_length=20)
    description = models.TextField('Descrição do Evento')
    preferred_date = models.DateField('Data Preferida')
    preferred_time = models.TimeField('Horário Preferido')
    estimated_duration = models.DurationField('Duração Estimada')
    location = models.CharField('Local', max_length=200, blank=True)
    budget = models.DecimalField(
        'Orçamento',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Status
    status = models.CharField(
        'Status',
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # Resposta do videomaker
    decline_reason = models.TextField('Motivo da Recusa', blank=True)

    # Timestamps
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    responded_at = models.DateTimeField('Respondido em', null=True, blank=True)

    class Meta:
        verbose_name = 'Solicitação de Agendamento'
        verbose_name_plural = 'Solicitações de Agendamento'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.client.full_name} → {self.videomaker.full_name}'

# ===========================================
# FILMERSHUB - MODELOS DE PAGAMENTOS
# ===========================================
# Pagamentos via Mercado Pago com split

from django.db import models
from django.conf import settings
import uuid


class Payment(models.Model):
    """
    Pagamento via Mercado Pago.
    Suporta PIX e Cartão de Crédito.
    Split: 85% videomaker / 15% plataforma.
    """

    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
        ('cancelled', 'Cancelado'),
        ('refunded', 'Reembolsado'),
    ]

    METHOD_CHOICES = [
        ('pix', 'PIX'),
        ('credit_card', 'Cartão de Crédito'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # Referência ao contrato
    contract = models.ForeignKey(
        'contracts.Contract',
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Contrato'
    )

    # Quem paga e quem recebe
    payer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments_made',
        verbose_name='Pagador'
    )

    payee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments_received',
        verbose_name='Recebedor'
    )

    # Valores
    total_amount = models.DecimalField(
        'Valor Total',
        max_digits=10,
        decimal_places=2
    )

    platform_fee = models.DecimalField(
        'Taxa Plataforma (15%)',
        max_digits=10,
        decimal_places=2
    )

    videomaker_amount = models.DecimalField(
        'Valor Videomaker (85%)',
        max_digits=10,
        decimal_places=2
    )

    # Método de pagamento
    payment_method = models.CharField(
        'Método',
        max_length=20,
        choices=METHOD_CHOICES,
        default='pix'
    )

    # Status
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # IDs do Mercado Pago
    mp_payment_id = models.CharField(
        'ID Pagamento MP',
        max_length=100,
        blank=True,
        unique=True
    )

    mp_preference_id = models.CharField(
        'ID Preferência MP',
        max_length=100,
        blank=True
    )

    mp_transaction_id = models.CharField(
        'ID Transação MP',
        max_length=100,
        blank=True
    )

    # Dados do cartão (últimos 4 dígitos)
    card_last_four = models.CharField(
        'Últimos 4 Dígitos Cartão',
        max_length=4,
        blank=True
    )

    # Data de pagamento
    paid_at = models.DateTimeField('Data do Pagamento', null=True, blank=True)

    # Notas
    notes = models.TextField('Observações', blank=True)

    # Timestamps
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.contract.contract_number} - R$ {self.total_amount}'

    def save(self, *args, **kwargs):
        """Calcula split automaticamente ao salvar."""
        if not self.platform_fee:
            self.platform_fee = self.total_amount * 0.15
            self.videomaker_amount = self.total_amount * 0.85
        super().save(*args, **kwargs)


class Refund(models.Model):
    """
    Reembolso de um pagamento.
    """

    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='refunds',
        verbose_name='Pagamento'
    )

    amount = models.DecimalField(
        'Valor do Reembolso',
        max_digits=10,
        decimal_places=2
    )

    reason = models.TextField('Motivo do Reembolso')

    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # ID do reembolso no Mercado Pago
    mp_refund_id = models.CharField(
        'ID Reembolso MP',
        max_length=100,
        blank=True
    )

    processed_at = models.DateTimeField('Processado em', null=True, blank=True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Reembolso'
        verbose_name_plural = 'Reembolsos'
        ordering = ['-created_at']

    def __str__(self):
        return f'Reembolso - {self.payment} - R$ {self.amount}'

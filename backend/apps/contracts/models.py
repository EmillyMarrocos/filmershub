# ===========================================
# FILMERSHUB - MODELOS DE CONTRATOS
# ===========================================
# Contratos profissionais com PDF e hash SHA-256

from django.db import models
from django.conf import settings
import uuid
import hashlib
import datetime


class Contract(models.Model):
    """
    Contrato profissional entre cliente e videomaker.
    Gera PDF com WeasyPrint e assina com SHA-256.
    """

    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('pending_signature', 'Aguardando Assinatura'),
        ('signed', 'Assinado'),
        ('in_progress', 'Em Andamento'),
        ('completed', 'Concluído'),
        ('cancelled', 'Cancelado'),
        ('expired', 'Expirado'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # Número sequencial do contrato (ex: FH-2026-00047)
    contract_number = models.CharField(
        'Número do Contrato',
        max_length=20,
        unique=True,
        editable=False
    )

    # Partes do contrato
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contracts_as_client',
        verbose_name='Cliente'
    )

    videomaker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contracts_as_videomaker',
        verbose_name='Videomaker'
    )

    # Detalhes do serviço
    SERVICE_TYPE_CHOICES = [
        ('wedding', 'Casamento'),
        ('corporate', 'Corporativo'),
        ('event', 'Evento'),
        ('music_video', 'Clipe Musical'),
        ('commercial', 'Comercial'),
        ('social_media', 'Redes Sociais'),
        ('other', 'Outro'),
    ]

    service_type = models.CharField(
        'Tipo de Serviço',
        max_length=20,
        choices=SERVICE_TYPE_CHOICES,
        default='other'
    )

    service_description = models.TextField('Descrição do Serviço')
    event_date = models.DateField('Data do Evento')
    delivery_date = models.DateField('Data de Entrega')
    location = models.CharField('Local do Evento', max_length=200)

    # Valores
    total_value = models.DecimalField(
        'Valor Total',
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        'Método de Pagamento',
        max_length=20        ,
        choices=[
            ('pix', 'PIX'),
            ('credit_card', 'Cartão de Crédito'),
            ('boleto', 'Boleto'),
            ('bank_transfer', 'Transferência Bancária'),
        ],
        default='pix'
    )

    # Status
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    # PDF do contrato
    pdf_file = models.FileField(
        'PDF do Contrato',
        upload_to='contracts/pdfs/',
        blank=True,
        null=True
    )

    # Hash SHA-256 do conteúdo do contrato
    content_hash = models.CharField(
        'Hash SHA-256',
        max_length=64,
        editable=False,
        blank=True
    )

    # Assinaturas digitais
    client_signed = models.BooleanField('Assinado pelo Cliente', default=False)
    videomaker_signed = models.BooleanField('Assinado pelo Videomaker', default=False)
    client_signed_at = models.DateTimeField('Data Assinatura Cliente', null=True, blank=True)
    videomaker_signed_at = models.DateTimeField('Data Assinatura Videomaker', null=True, blank=True)

    # Cláusulas adicionais
    additional_clauses = models.TextField('Cláusulas Adicionais', blank=True)

    # Notas
    internal_notes = models.TextField('Notas Internas', blank=True)

    # Timestamps
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.contract_number} - {self.client.full_name} ↔ {self.videomaker.full_name}'

    def save(self, *args, **kwargs):
        """Gera número do contrato e hash ao salvar."""
        if not self.contract_number:
            # Gera número: FH-ANO-XXXXX
            year = datetime.datetime.now().year
            last_contract = Contract.objects.filter(
                contract_number__startswith=f'FH-{year}'
            ).order_by('-contract_number').first()

            if last_contract:
                last_number = int(last_contract.contract_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1

            self.contract_number = f'FH-{year}-{new_number:05d}'

        # Gera hash SHA-256 do conteúdo
        content = f'{self.contract_number}{self.client_id}{self.videomaker_id}{self.total_value}{self.event_date}'
        self.content_hash = hashlib.sha256(content.encode()).hexdigest()

        super().save(*args, **kwargs)


class ContractClause(models.Model):
    """
    Cláusulas do contrato.
    Cada cláusula é um parágrafo do contrato.
    """

    CLAUSE_CHOICES = [
        ('scope', 'Escopo do Serviço'),
        ('payment', 'Condições de Pagamento'),
        ('delivery', 'Prazo de Entrega'),
        ('cancellation', 'Cancelamento'),
        ('confidentiality', 'Sigilo'),
        ('copyright', 'Direitos Autorais'),
        ('liability', 'Responsabilidade'),
        ('revision', 'Revisões'),
        ('force_majeure', 'Força Maior'),
        ('jurisdiction', 'Foro'),
        ('additional', 'Adicional'),
    ]

    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name='clauses',
        verbose_name='Contrato'
    )

    clause_type = models.CharField(
        'Tipo da Cláusula',
        max_length=20,
        choices=CLAUSE_CHOICES
    )

    title = models.CharField('Título', max_length=200)
    content = models.TextField('Conteúdo')
    order = models.PositiveIntegerField('Ordem', default=0)

    class Meta:
        verbose_name = 'Cláusula do Contrato'
        verbose_name_plural = 'Cláusulas do Contrato'
        ordering = ['order']
        unique_together = ('contract', 'clause_type')

    def __str__(self):
        return f'{self.contract.contract_number} - {self.title}'

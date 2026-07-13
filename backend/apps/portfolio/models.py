# ===========================================
# FILMERSHUB - MODELOS DE PORTFÓLIO
# ===========================================
# Trabalhos, categorias e avaliações

from django.db import models
from django.conf import settings
import uuid


class Category(models.Model):
    """Categorias de trabalhos (Casamento, Corporativo, etc.)"""

    name = models.CharField('Nome', max_length=100, unique=True)
    slug = models.SlugField('Slug', max_length=100, unique=True)
    description = models.TextField('Descrição', blank=True)
    icon = models.CharField('Ícone', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return self.name


class Work(models.Model):
    """
    Trabalho no portfólio de um videomaker.
    Pode ser: vídeo, foto, ou ambos.
    """

    TYPE_CHOICES = [
        ('video', 'Vídeo'),
        ('photo', 'Foto'),
        ('mixed', 'Misto'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
        ('archived', 'Arquivado'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    videomaker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='works',
        verbose_name='Videomaker'
    )

    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição', max_length=2000)
    work_type = models.CharField(
        'Tipo',
        max_length=10,
        choices=TYPE_CHOICES,
        default='video'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='works',
        verbose_name='Categoria'
    )

    # Arquivo principal (vídeo ou foto)
    file = models.FileField(
        'Arquivo',
        upload_to='works/files/',
        blank=True,
        null=True
    )

    # Thumbnail (imagem de capa)
    thumbnail = models.ImageField(
        'Thumbnail',
        upload_to='works/thumbnails/',
        blank=True,
        null=True
    )

    # URL externa (YouTube, Vimeo, etc.)
    external_url = models.URLField('URL Externa', blank=True)

    # Metadados
    client_name = models.CharField('Nome do Cliente', max_length=200, blank=True)
    location = models.CharField('Localização', max_length=200, blank=True)
    equipment_used = models.TextField('Equipamentos Utilizados', blank=True)

    # Estatísticas
    views_count = models.PositiveIntegerField('Visualizações', default=0)
    likes_count = models.PositiveIntegerField('Curtidas', default=0)

    # Status
    status = models.CharField(
        'Status',
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )

    # Timestamps
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    published_at = models.DateTimeField('Publicado em', null=True, blank=True)

    class Meta:
        verbose_name = 'Trabalho'
        verbose_name_plural = 'Trabalhos'
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return f'{self.title} - {self.videomaker.full_name}'


class WorkMedia(models.Model):
    """Mídias adicionais de um trabalho (fotos extras, vídeos extras)."""

    TYPE_CHOICES = [
        ('image', 'Imagem'),
        ('video', 'Vídeo'),
    ]

    work = models.ForeignKey(
        Work,
        on_delete=models.CASCADE,
        related_name='media',
        verbose_name='Trabalho'
    )

    file = models.FileField(
        'Arquivo',
        upload_to='works/media/'
    )

    media_type = models.CharField(
        'Tipo',
        max_length=10,
        choices=TYPE_CHOICES,
        default='image'
    )

    caption = models.CharField('Legenda', max_length=200, blank=True)
    order = models.PositiveIntegerField('Ordem', default=0)

    class Meta:
        verbose_name = 'Mídia do Trabalho'
        verbose_name_plural = 'Mídias do Trabalho'
        ordering = ['order']

    def __str__(self):
        return f'{self.media_type} - {self.work.title}'


class Review(models.Model):
    """
    Avaliação de um cliente sobre um videomaker.
    Feita após a conclusão de um contrato.
    """

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_given',
        verbose_name='Avaliador'
    )

    videomaker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_received',
        verbose_name='Videomaker'
    )

    work = models.ForeignKey(
        Work,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
        verbose_name='Trabalho'
    )

    rating = models.IntegerField(
        'Nota',
        choices=RATING_CHOICES,
        help_text='De 1 a 5'
    )

    comment = models.TextField('Comentário', max_length=1000, blank=True)

    # Resposta do videomaker (opcional)
    response = models.TextField('Resposta', max_length=1000, blank=True)
    responded_at = models.DateTimeField('Respondido em', null=True, blank=True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        unique_together = ('reviewer', 'videomaker', 'work')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.reviewer.full_name} → {self.videomaker.full_name} ({self.rating}★)'

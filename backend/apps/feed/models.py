# ===========================================
# FILMERSHUB - MODELOS DO FEED
# ===========================================
# Posts, curtidas e comentários

from django.db import models
from django.conf import settings
import uuid


class Post(models.Model):
    """
    Post no feed social.
    Videomakers podem compartilhar bastidores, dicas, etc.
    """

    TYPE_CHOICES = [
        ('text', 'Texto'),
        ('image', 'Imagem'),
        ('video', 'Vídeo'),
        ('link', 'Link'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Autor'
    )

    content = models.TextField('Conteúdo', max_length=5000)
    post_type = models.CharField(
        'Tipo',
        max_length=10,
        choices=TYPE_CHOICES,
        default='text'
    )

    # Mídia (opcional)
    media = models.FileField(
        'Mídia',
        upload_to='posts/media/',
        blank=True,
        null=True
    )

    # Link externo (opcional)
    link_url = models.URLField('URL do Link', blank=True)
    link_title = models.CharField('Título do Link', max_length=200, blank=True)
    link_description = models.TextField('Descrição do Link', blank=True)

    # Estatísticas
    likes_count = models.PositiveIntegerField('Curtidas', default=0)
    comments_count = models.PositiveIntegerField('Comentários', default=0)
    shares_count = models.PositiveIntegerField('Compartilhamentos', default=0)

    # Timestamps
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author.full_name} - {self.content[:50]}...'


class Like(models.Model):
    """Curtida em um post."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Usuário'
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Post'
    )

    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Curtida'
        verbose_name_plural = 'Curtidas'
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user.full_name} curtiu {self.post.id}'


class Comment(models.Model):
    """Comentário em um post."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Autor'
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Post'
    )

    # Comentário pai (para respostas aninhadas)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='Comentário Pai'
    )

    content = models.TextField('Conteúdo', max_length=2000)

    likes_count = models.PositiveIntegerField('Curtidas', default=0)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author.full_name} em {self.post.id}'

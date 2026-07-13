# ===========================================
# FILMERSHUB - MODELOS DE CONTA
# ===========================================
# Modelo customizado de usuário
# Um usuário pode ser VIDEOMAKER, CLIENT ou AMBOS

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
import uuid


class UserManager(BaseUserManager):
    """Gerenciador customizado de usuários."""

    def create_user(self, email, password=None, **extra_fields):
        """Cria e retorna um usuário com email e senha."""
        if not email:
            raise ValueError('O campo email é obrigatório')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Cria e retorna um superusuário."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário precisa ter is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário precisa ter is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modelo customizado de usuário.
    Substitui o padrão do Django (que usa username por email).
    Um usuário pode ser VIDEOMAKER, CLIENT ou AMBOS ao mesmo tempo.
    """

    # Tipos de perfil
    class ProfileType(models.TextChoices):
        VIDEOMAKER = 'videomaker', 'Videomaker'
        CLIENT = 'client', 'Cliente'
        BOTH = 'both', 'Ambos'

    # ID único (UUID)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID'
    )

    # Dados pessoais
    first_name = models.CharField('Nome', max_length=150)
    last_name = models.CharField('Sobrenome', max_length=150)
    email = models.EmailField('Email', unique=True)

    # Tipo de perfil (pode ser AMBOS ao mesmo tempo)
    profile_type = models.CharField(
        'Tipo de Perfil',
        max_length=10,
        choices=ProfileType.choices,
        default=ProfileType.BOTH
    )

    # CPF ou CNPJ (obrigatório para contratos)
    cpf_cnpj = models.CharField(
        'CPF/CNPJ',
        max_length=18,
        unique=True,
        null=True,
        blank=True,
        help_text='CPF: XXX.XXX.XXX-XX ou CNPJ: XX.XXX.XXX/XXXX-XX'
    )

    # Telefone
    phone = models.CharField('Telefone', max_length=20, blank=True)

    # Avatar (foto de perfil)
    avatar = models.ImageField(
        'Avatar',
        upload_to='avatars/',
        blank=True,
        null=True
    )

    # Biografia
    bio = models.TextField('Biografia', max_length=500, blank=True)

    # Localização
    city = models.CharField('Cidade', max_length=100, blank=True)
    state = models.CharField('Estado', max_length=2, blank=True)

    # Redes sociais
    instagram = models.CharField('Instagram', max_length=100, blank=True)
    youtube = models.CharField('YouTube', max_length=100, blank=True)
    website = models.URLField('Website', blank=True)

    # Configurações
    is_videomaker = models.BooleanField('É Videomaker', default=False)
    is_client = models.BooleanField('É Cliente', default=False)
    is_active = models.BooleanField('Ativo', default=True)
    is_staff = models.BooleanField('Staff', default=False)

    # Reset de senha
    reset_token = models.CharField('Token de Reset', max_length=64, blank=True, null=True, unique=True)
    reset_token_expires = models.DateTimeField('Expiração do Token', null=True, blank=True)

    # Timestamps
    date_joined = models.DateTimeField('Data de Cadastro', default=timezone.now)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    # Configurações do Django
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        """Retorna o nome completo do usuário."""
        return f'{self.first_name} {self.last_name}'

    @property
    def is_videomaker_only(self):
        """Verifica se o usuário é apenas videomaker."""
        return self.profile_type == self.ProfileType.VIDEOMAKER

    @property
    def is_client_only(self):
        """Verifica se o usuário é apenas cliente."""
        return self.profile_type == self.ProfileType.CLIENT

    @property
    def is_both(self):
        """Verifica se o usuário é AMBOS (videomaker e cliente)."""
        return self.profile_type == self.ProfileType.BOTH

    def save(self, *args, **kwargs):
        """Sobrescreve o save para garantir consistência dos tipos."""
        # Se profile_type é BOTH, ativa as duas flags
        if self.profile_type == self.ProfileType.BOTH:
            self.is_videomaker = True
            self.is_client = True
        elif self.profile_type == self.ProfileType.VIDEOMAKER:
            self.is_videomaker = True
            self.is_client = False
        elif self.profile_type == self.ProfileType.CLIENT:
            self.is_videomaker = False
            self.is_client = True

        super().save(*args, **kwargs)


class VideomakerProfile(models.Model):
    """
    Perfil estendido de videomaker.
    Contém informações específicas para profissionais de vídeo.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='videomaker_profile',
        verbose_name='Usuário'
    )

    # Especialidades
    SPECIALTY_CHOICES = [
        ('wedding', 'Casamento'),
        ('corporate', 'Corporativo'),
        ('event', 'Eventos'),
        ('music_video', 'Clipe Musical'),
        ('documentary', 'Documentário'),
        ('commercial', 'Comercial'),
        ('social_media', 'Redes Sociais'),
        ('other', 'Outro'),
    ]

    specialty = models.CharField(
        'Especialidade Principal',
        max_length=20,
        choices=SPECIALTY_CHOICES,
        blank=True
    )

    # Preços
    hourly_rate = models.DecimalField(
        'Valor Hora',
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Valor cobrado por hora de trabalho'
    )

    day_rate = models.DecimalField(
        'Valor Diária',
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Valor cobrado por dia de trabalho'
    )

    # Disponibilidade
    is_available = models.BooleanField('Disponível', default=True)
    travel_radius = models.IntegerField(
        'Raio de Atendimento (km)',
        default=50,
        help_text='Distância máxima que está disposto a viajar'
    )

    # Estatísticas (atualizadas por signals)
    total_jobs = models.IntegerField('Total de Trabalhos', default=0)
    average_rating = models.DecimalField(
        'Avaliação Média',
        max_digits=3,
        decimal_places=1,
        default=0.0
    )
    total_reviews = models.IntegerField('Total de Avaliações', default=0)

    # Timestamps
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Perfil Videomaker'
        verbose_name_plural = 'Perfis Videomakers'
        ordering = ['-average_rating', '-total_jobs']

    def __str__(self):
        return f'Videomaker: {self.user.full_name}'


class ClientProfile(models.Model):
    """
    Perfil estendido de cliente.
    Contém informações específicas para clientes que contratam videomakers.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='client_profile',
        verbose_name='Usuário'
    )

    # Tipo de cliente
    CLIENT_TYPE_CHOICES = [
        ('individual', 'Pessoa Física'),
        ('company', 'Empresa'),
        ('agency', 'Agência'),
    ]

    client_type = models.CharField(
        'Tipo de Cliente',
        max_length=20,
        choices=CLIENT_TYPE_CHOICES,
        default='individual'
    )

    # Nome da empresa (se aplicável)
    company_name = models.CharField('Nome da Empresa', max_length=200, blank=True)

    # CNPJ da empresa (se aplicável)
    company_cnpj = models.CharField('CNPJ da Empresa', max_length=18, blank=True)

    # Quantidade de contratos realizados
    total_contracts = models.IntegerField('Total de Contratos', default=0)

    # Timestamps
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Perfil Cliente'
        verbose_name_plural = 'Perfis Clientes'
        ordering = ['-total_contracts']

    def __str__(self):
        return f'Cliente: {self.user.full_name}'


class Follow(models.Model):
    """
    Relação de seguir entre usuários.
    Permite que clientes sigam videomakers e vice-versa.
    """

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Seguidor'
    )

    followed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Seguindo'
    )

    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Seguidor'
        verbose_name_plural = 'Seguidores'
        unique_together = ('follower', 'followed')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.follower.full_name} segue {self.followed.full_name}'

    def save(self, *args, **kwargs):
        """Impede que um usuário siga a si mesmo."""
        if self.follower == self.followed:
            raise ValueError('Um usuário não pode seguir a si mesmo')
        super().save(*args, **kwargs)


class Skill(models.Model):
    """
    Habilidades de videomaker.
    Ex: Edição, Cinegrafismo, Color Grading, etc.
    """

    name = models.CharField('Nome', max_length=100, unique=True)
    slug = models.SlugField('Slug', max_length=100, unique=True)
    description = models.TextField('Descrição', blank=True)

    class Meta:
        verbose_name = 'Habilidade'
        verbose_name_plural = 'Habilidades'
        ordering = ['name']

    def __str__(self):
        return self.name


class VideomakerSkill(models.Model):
    """
    Habilidade associada a um videomaker.
    """

    videomaker = models.ForeignKey(
        VideomakerProfile,
        on_delete=models.CASCADE,
        related_name='skills',
        verbose_name='Videomaker'
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='videomakers',
        verbose_name='Habilidade'
    )

    # Nível de experiência (1-5)
    EXPERIENCE_LEVEL_CHOICES = [
        (1, 'Iniciante'),
        (2, 'Básico'),
        (3, 'Intermediário'),
        (4, 'Avançado'),
        (5, 'Especialista'),
    ]

    experience_level = models.IntegerField(
        'Nível de Experiência',
        choices=EXPERIENCE_LEVEL_CHOICES,
        default=3
    )

    class Meta:
        verbose_name = 'Habilidade do Videomaker'
        verbose_name_plural = 'Habilidades dos Videomakers'
        unique_together = ('videomaker', 'skill')

    def __str__(self):
        return f'{self.skill.name} - {self.videomaker.user.full_name}'

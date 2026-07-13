# ===========================================
# FILMERSHUB - ADMIN DE CONTAS
# ===========================================
# Painel administrativo para gerenciar usuários

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, VideomakerProfile, ClientProfile, Follow, Skill, VideomakerSkill


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin customizado para o modelo User."""

    # Colunas que aparecem na lista
    list_display = (
        'email', 'first_name', 'last_name',
        'profile_type', 'is_active', 'is_staff', 'date_joined'
    )

    # Filtros laterais
    list_filter = (
        'is_active', 'is_staff', 'is_superuser',
        'profile_type', 'date_joined'
    )

    # Campo de busca
    search_fields = ('email', 'first_name', 'last_name')

    # Ordenação padrão
    ordering = ('-date_joined',)

    # Campos do formulário de edição
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Dados Pessoais', {
            'fields': ('first_name', 'last_name', 'phone', 'avatar', 'bio')
        }),
        ('Localização', {
            'fields': ('city', 'state')
        }),
        ('Redes Sociais', {
            'fields': ('instagram', 'youtube', 'website')
        }),
        ('Tipo de Perfil', {
            'fields': ('profile_type', 'is_videomaker', 'is_client', 'cpf_cnpj')
        }),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Datas Importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Campos ao criar novo usuário
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name',
                'password1', 'password2',
                'profile_type'
            ),
        }),
    )


@admin.register(VideomakerProfile)
class VideomakerProfileAdmin(admin.ModelAdmin):
    """Admin para perfis de videomaker."""

    list_display = (
        'user', 'specialty', 'hourly_rate', 'day_rate',
        'is_available', 'average_rating', 'total_jobs'
    )

    list_filter = ('specialty', 'is_available')

    search_fields = ('user__email', 'user__first_name', 'user__last_name')


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    """Admin para perfis de cliente."""

    list_display = (
        'user', 'client_type', 'company_name', 'total_contracts'
    )

    list_filter = ('client_type',)

    search_fields = ('user__email', 'user__first_name', 'user__last_name')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Admin para seguidores."""

    list_display = ('follower', 'followed', 'created_at')

    search_fields = (
        'follower__email', 'follower__first_name',
        'followed__email', 'followed__first_name'
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Admin para habilidades."""

    list_display = ('name', 'slug')

    search_fields = ('name',)


@admin.register(VideomakerSkill)
class VideomakerSkillAdmin(admin.ModelAdmin):
    """Admin para habilidades de videomaker."""

    list_display = ('videomaker', 'skill', 'experience_level')

    list_filter = ('experience_level',)

    search_fields = (
        'videomaker__user__email',
        'skill__name'
    )

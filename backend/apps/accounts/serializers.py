# ===========================================
# FILMERSHUB - SERIALIZERS DE USUÁRIO
# ===========================================

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import VideomakerProfile, ClientProfile, Follow, Skill, VideomakerSkill

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer para dados do usuário."""

    full_name = serializers.ReadOnlyField()
    avatar_url = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'profile_type', 'phone', 'avatar', 'avatar_url',
            'bio', 'city', 'state',
            'instagram', 'youtube', 'website',
            'is_videomaker', 'is_client', 'is_following', 'followers_count',
            'date_joined',
        ]
        read_only_fields = ['id', 'email', 'date_joined', 'profile_type', 'is_videomaker', 'is_client']

    def get_avatar_url(self, obj):
        """Retorna URL do avatar."""
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user != obj:
            return Follow.objects.filter(follower=request.user, followed=obj).exists()
        return False

    def get_followers_count(self, obj):
        return Follow.objects.filter(followed=obj).count()


class UserListSerializer(serializers.ModelSerializer):
    """Serializer leve para listagem de usuários."""

    full_name = serializers.ReadOnlyField()
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'full_name', 'avatar_url', 'profile_type', 'bio', 'city', 'state']

    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None


class PublicProfileSerializer(serializers.ModelSerializer):
    """Serializer público - esconde dados sensíveis (email, phone)."""

    full_name = serializers.ReadOnlyField()
    avatar_url = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'full_name',
            'profile_type', 'avatar', 'avatar_url',
            'bio', 'city', 'state',
            'instagram', 'youtube', 'website',
            'is_videomaker', 'is_client', 'is_following', 'followers_count',
            'date_joined',
        ]

    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user != obj:
            return Follow.objects.filter(follower=request.user, followed=obj).exists()
        return False

    def get_followers_count(self, obj):
        return Follow.objects.filter(followed=obj).count()


class VideomakerProfileSerializer(serializers.ModelSerializer):
    """Serializer para perfil de videomaker."""

    user = UserSerializer(read_only=True)
    skills = serializers.SerializerMethodField()

    class Meta:
        model = VideomakerProfile
        fields = [
            'id', 'user', 'specialty', 'hourly_rate', 'day_rate',
            'is_available', 'travel_radius',
            'total_jobs', 'average_rating', 'total_reviews',
            'skills',
        ]

    def get_skills(self, obj):
        """Retorna habilidades do videomaker."""
        skills = obj.skills.all()
        return VideomakerSkillSerializer(skills, many=True).data


class VideomakerProfileCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para criar/atualizar perfil de videomaker."""

    class Meta:
        model = VideomakerProfile
        fields = [
            'specialty', 'hourly_rate', 'day_rate',
            'is_available', 'travel_radius',
        ]


class ClientProfileSerializer(serializers.ModelSerializer):
    """Serializer para perfil de cliente."""

    user = UserSerializer(read_only=True)

    class Meta:
        model = ClientProfile
        fields = [
            'id', 'user', 'client_type', 'company_name',
            'total_contracts',
        ]


class ClientProfileCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para criar/atualizar perfil de cliente."""

    class Meta:
        model = ClientProfile
        fields = ['client_type', 'company_name', 'company_cnpj']


class FollowSerializer(serializers.ModelSerializer):
    """Serializer para seguidores."""

    follower = UserListSerializer(read_only=True)
    followed = UserListSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed', 'created_at']


class SkillSerializer(serializers.ModelSerializer):
    """Serializer para habilidades."""

    class Meta:
        model = Skill
        fields = ['id', 'name', 'slug', 'description']


class VideomakerSkillSerializer(serializers.ModelSerializer):
    """Serializer para habilidade de videomaker."""

    skill = SkillSerializer(read_only=True)

    class Meta:
        model = VideomakerSkill
        fields = ['id', 'skill', 'experience_level']

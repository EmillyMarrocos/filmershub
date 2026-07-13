# ===========================================
# FILMERSHUB - TESTES DE SERIALIZERS (ACCOUNTS)
# ===========================================

import pytest
from django.contrib.auth import get_user_model
from apps.accounts.serializers import UserSerializer, VideomakerProfileSerializer
from apps.accounts.serializers_auth import RegisterSerializer

User = get_user_model()


@pytest.mark.django_db
class TestRegisterSerializer:
    """Testes para o serializer de registro."""

    def test_valid_data(self):
        """Testa dados válidos."""
        data = {
            'email': 'novo@test.com',
            'first_name': 'Novo',
            'last_name': 'Usuario',
            'password': 'senha12345',
            'password_confirm': 'senha12345',
            'profile_type': 'both',
        }
        serializer = RegisterSerializer(data=data)
        assert serializer.is_valid()

    def test_password_mismatch(self):
        """Testa senhas diferentes."""
        data = {
            'email': 'novo@test.com',
            'first_name': 'Novo',
            'last_name': 'Usuario',
            'password': 'senha12345',
            'password_confirm': 'outrasenha',
            'profile_type': 'both',
        }
        serializer = RegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password_confirm' in serializer.errors

    def test_create_user(self):
        """Testa criação de usuário."""
        data = {
            'email': 'novo@test.com',
            'first_name': 'Novo',
            'last_name': 'Usuario',
            'password': 'senha12345',
            'password_confirm': 'senha12345',
            'profile_type': 'videomaker',
        }
        serializer = RegisterSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.email == 'novo@test.com'
        assert user.is_videomaker is True


@pytest.mark.django_db
class TestUserSerializer:
    """Testes para o serializer de usuário."""

    def test_serialize_user(self, user):
        """Testa serialização de usuário."""
        serializer = UserSerializer(user)
        data = serializer.data
        assert data['email'] == user.email
        assert data['first_name'] == user.first_name
        assert 'password' not in data

    def test_read_only_fields(self, user):
        """Testa campos somente leitura."""
        serializer = UserSerializer(user)
        assert 'id' in serializer.data
        assert 'date_joined' in serializer.data


@pytest.mark.django_db
class TestVideomakerProfileSerializer:
    """Testes para o serializer de perfil videomaker."""

    def test_serialize_profile(self, videomaker_user):
        """Testa serialização de perfil."""
        from apps.accounts.models import VideomakerProfile
        profile = VideomakerProfile.objects.create(
            user=videomaker_user,
            specialty='wedding',
        )
        serializer = VideomakerProfileSerializer(profile)
        data = serializer.data
        assert data['specialty'] == 'wedding'
        assert 'user' in data

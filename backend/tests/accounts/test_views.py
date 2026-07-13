# ===========================================
# FILMERSHUB - TESTES DE VIEWS (ACCOUNTS API)
# ===========================================

import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestRegisterView:
    """Testes para o endpoint de registro."""

    def test_register_success(self, api_client):
        """Testa registro bem-sucedido."""
        url = reverse('register')
        data = {
            'email': 'novo@test.com',
            'first_name': 'Novo',
            'last_name': 'Usuario',
            'password': 'senha12345',
            'password_confirm': 'senha12345',
            'profile_type': 'both',
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'tokens' in response.data
        assert 'user' in response.data

    def test_register_password_mismatch(self, api_client):
        """Testa registro com senhas diferentes."""
        url = reverse('register')
        data = {
            'email': 'novo@test.com',
            'first_name': 'Novo',
            'last_name': 'Usuario',
            'password': 'senha12345',
            'password_confirm': 'outrasenha',
            'profile_type': 'both',
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_duplicate_email(self, api_client, user):
        """Testa registro com email duplicado."""
        url = reverse('register')
        data = {
            'email': user.email,
            'first_name': 'Outro',
            'last_name': 'Usuario',
            'password': 'senha12345',
            'password_confirm': 'senha12345',
            'profile_type': 'client',
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLoginView:
    """Testes para o endpoint de login."""

    def test_login_success(self, api_client, user):
        """Testa login bem-sucedido."""
        url = reverse('token_obtain_pair')
        data = {
            'email': user.email,
            'password': 'testpass123',
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_wrong_password(self, api_client, user):
        """Testa login com senha errada."""
        url = reverse('token_obtain_pair')
        data = {
            'email': user.email,
            'password': 'senhaerrada',
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, api_client):
        """Testa login com usuário inexistente."""
        url = reverse('token_obtain_pair')
        data = {
            'email': 'naoexiste@test.com',
            'password': 'senha123',
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserProfileView:
    """Testes para o endpoint de perfil do usuário."""

    def test_get_profile(self, authenticated_client, user):
        """Testa busca de perfil."""
        url = reverse('user-profile')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email

    def test_update_profile(self, authenticated_client, user):
        """Testa atualização de perfil."""
        url = reverse('user-profile')
        data = {'bio': 'Nova biografia'}
        response = authenticated_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.bio == 'Nova biografia'

    def test_profile_unauthorized(self, api_client):
        """Testa acesso sem autenticação."""
        url = reverse('user-profile')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestVideomakerListView:
    """Testes para o endpoint de listagem de videomakers."""

    def test_list_videomakers(self, api_client, videomaker_user):
        """Testa listagem de videomakers."""
        url = reverse('videomaker-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_videomakers_search(self, api_client, videomaker_user):
        """Testa busca de videomakers."""
        url = reverse('videomaker-list')
        response = api_client.get(url, {'search': 'John'})
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestFollowToggleView:
    """Testes para o endpoint de seguir/deixar de seguir."""

    def test_follow_user(self, authenticated_client, videomaker_user):
        """Testa seguir um usuário."""
        url = reverse('follow-toggle', kwargs={'id': videomaker_user.id})
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_201_CREATED

    def test_unfollow_user(self, authenticated_client, user, videomaker_user):
        """Testa deixar de seguir um usuário."""
        from apps.accounts.models import Follow
        Follow.objects.create(follower=user, followed=videomaker_user)

        url = reverse('follow-toggle', kwargs={'id': videomaker_user.id})
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK

    def test_cannot_follow_self(self, authenticated_client, user):
        """Testa que não pode seguir a si mesmo."""
        url = reverse('follow-toggle', kwargs={'id': user.id})
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

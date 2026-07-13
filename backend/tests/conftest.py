# ===========================================
# FILMERSHUB - CONFTEST.PY
# ===========================================
# Fixtures compartilhadas entre todos os testes

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    """Cliente API para testes."""
    return APIClient()


@pytest.fixture
def user(db):
    """Usuário padrão para testes."""
    return User.objects.create_user(
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User',
        profile_type='both',
    )


@pytest.fixture
def videomaker_user(db):
    """Usuário videomaker para testes."""
    return User.objects.create_user(
        email='videomaker@example.com',
        password='testpass123',
        first_name='John',
        last_name='Doe',
        profile_type='videomaker',
    )


@pytest.fixture
def client_user(db):
    """Usuário cliente para testes."""
    return User.objects.create_user(
        email='client@example.com',
        password='testpass123',
        first_name='Jane',
        last_name='Smith',
        profile_type='client',
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Cliente API autenticado."""
    api_client.force_authenticate(user=user)
    return api_client

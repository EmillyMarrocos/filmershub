# ===========================================
# FILMERSHUB - TESTES DE VIEWS (PORTFOLIO API)
# ===========================================

import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.portfolio.models import Category, Work

User = get_user_model()


@pytest.mark.django_db
class TestCategoryListView:
    """Testes para o endpoint de categorias."""

    def test_list_categories(self, api_client):
        """Testa listagem de categorias."""
        Category.objects.create(name='Casamento', slug='casamento')
        url = reverse('category-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_categories_empty(self, api_client):
        """Testa listagem vazia."""
        url = reverse('category-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestWorkListView:
    """Testes para o endpoint de trabalhos."""

    def test_list_works(self, api_client, videomaker_user):
        """Testa listagem de trabalhos publicados."""
        Work.objects.create(
            videomaker=videomaker_user,
            title='Trabalho 1',
            description='Descrição',
            status='published',
        )
        url = reverse('work-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_list_only_published(self, api_client, videomaker_user):
        """Testa que só mostra trabalhos publicados."""
        Work.objects.create(
            videomaker=videomaker_user,
            title='Rascunho',
            description='Descrição',
            status='draft',
        )
        Work.objects.create(
            videomaker=videomaker_user,
            title='Publicado',
            description='Descrição',
            status='published',
        )
        url = reverse('work-list')
        response = api_client.get(url)
        assert response.data['count'] == 1


@pytest.mark.django_db
class TestWorkCreateView:
    """Testes para criação de trabalho."""

    def test_create_work(self, authenticated_client, videomaker_user):
        """Testa criação de trabalho."""
        url = reverse('work-list')
        data = {
            'title': 'Novo Trabalho',
            'description': 'Descrição do trabalho',
            'work_type': 'video',
        }
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_work_unauthorized(self, api_client):
        """Testa criação sem autenticação."""
        url = reverse('work-list')
        data = {
            'title': 'Trabalho',
            'description': 'Descrição',
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestWorkDetailView:
    """Testes para detalhe de trabalho."""

    def test_get_work(self, api_client, videomaker_user):
        """Testa busca de trabalho."""
        work = Work.objects.create(
            videomaker=videomaker_user,
            title='Trabalho',
            description='Descrição',
            status='published',
        )
        url = reverse('work-detail', kwargs={'pk': work.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_increment_views(self, api_client, videomaker_user):
        """Testa incremento de visualizações."""
        work = Work.objects.create(
            videomaker=videomaker_user,
            title='Trabalho',
            description='Descrição',
            status='published',
        )
        url = reverse('work-detail', kwargs={'pk': work.id})
        api_client.get(url)
        work.refresh_from_db()
        assert work.views_count == 1

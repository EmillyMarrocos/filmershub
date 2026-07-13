# ===========================================
# FILMERSHUB - TESTES DE VIEWS (FEED API)
# ===========================================

import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.feed.models import Post, Like, Comment

User = get_user_model()


@pytest.mark.django_db
class TestPostListView:
    """Testes para o endpoint de listagem de posts."""

    def test_list_posts(self, api_client, user):
        """Testa listagem de posts."""
        Post.objects.create(author=user, content='Post 1')
        Post.objects.create(author=user, content='Post 2')
        url = reverse('post-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestPostCreateView:
    """Testes para criação de post."""

    def test_create_post(self, authenticated_client, user):
        """Testa criação de post."""
        url = reverse('post-create')
        data = {
            'content': 'Novo post!',
            'post_type': 'text',
        }
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_post_unauthorized(self, api_client):
        """Testa criação sem autenticação."""
        url = reverse('post-create')
        data = {'content': 'Post', 'post_type': 'text'}
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestLikeToggleView:
    """Testes para curtir/descurtir."""

    def test_like_post(self, authenticated_client, user):
        """Testa curtir um post."""
        post = Post.objects.create(author=user, content='Post')
        url = reverse('like-toggle', kwargs={'post_id': post.id})
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_201_CREATED
        post.refresh_from_db()
        assert post.likes_count == 1

    def test_unlike_post(self, authenticated_client, user):
        """Testa descurtir um post."""
        post = Post.objects.create(author=user, content='Post')
        Like.objects.create(user=user, post=post)
        url = reverse('like-toggle', kwargs={'post_id': post.id})
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        post.refresh_from_db()
        assert post.likes_count == 0


@pytest.mark.django_db
class TestCommentCreateView:
    """Testes para criação de comentário."""

    def test_create_comment(self, authenticated_client, user):
        """Testa criação de comentário."""
        post = Post.objects.create(author=user, content='Post')
        url = reverse('comment-create', kwargs={'post_id': post.id})
        data = {'content': 'Bom post!'}
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        post.refresh_from_db()
        assert post.comments_count == 1

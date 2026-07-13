# ===========================================
# FILMERSHUB - TESTES DE MODELOS (FEED)
# ===========================================

import pytest
from django.contrib.auth import get_user_model
from apps.feed.models import Post, Like, Comment

User = get_user_model()


@pytest.mark.django_db
class TestPost:
    """Testes para o modelo Post."""

    def test_create_post(self, user):
        """Testa criação de post."""
        post = Post.objects.create(
            author=user,
            content='Meu primeiro post!',
            post_type='text',
        )
        assert post.content == 'Meu primeiro post!'
        assert post.author == user

    def test_post_str(self, user):
        """Testa representação string."""
        post = Post(
            author=user,
            content='Texto curto',
        )
        assert 'Test User' in str(post)

    def test_post_default_values(self, user):
        """Testa valores padrão."""
        post = Post.objects.create(
            author=user,
            content='Teste',
        )
        assert post.likes_count == 0
        assert post.comments_count == 0


@pytest.mark.django_db
class TestLike:
    """Testes para o modelo Like."""

    def test_create_like(self, user):
        """Testa criação de curtida."""
        post = Post.objects.create(author=user, content='Post')
        like = Like.objects.create(user=user, post=post)
        assert like.user == user
        assert like.post == post

    def test_unique_like(self, user):
        """Testa que não pode curtir duas vezes."""
        post = Post.objects.create(author=user, content='Post')
        Like.objects.create(user=user, post=post)
        with pytest.raises(Exception):
            Like.objects.create(user=user, post=post)


@pytest.mark.django_db
class TestComment:
    """Testes para o modelo Comment."""

    def test_create_comment(self, user):
        """Testa criação de comentário."""
        post = Post.objects.create(author=user, content='Post')
        comment = Comment.objects.create(
            author=user,
            post=post,
            content='Bom post!',
        )
        assert comment.content == 'Bom post!'

    def test_comment_reply(self, user):
        """Testa resposta a comentário."""
        post = Post.objects.create(author=user, content='Post')
        parent = Comment.objects.create(
            author=user,
            post=post,
            content='Comentário original',
        )
        reply = Comment.objects.create(
            author=user,
            post=post,
            parent=parent,
            content='Resposta',
        )
        assert reply.parent == parent
        assert parent.replies.count() == 1

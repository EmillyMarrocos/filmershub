# ===========================================
# FILMERSHUB - TESTES DE MODELOS (PORTFOLIO)
# ===========================================

import pytest
from django.contrib.auth import get_user_model
from apps.portfolio.models import Category, Work, WorkMedia, Review

User = get_user_model()


@pytest.mark.django_db
class TestCategory:
    """Testes para o modelo Category."""

    def test_create_category(self):
        """Testa criação de categoria."""
        category = Category.objects.create(
            name='Casamento',
            slug='casamento',
        )
        assert category.name == 'Casamento'

    def test_category_str(self):
        """Testa representação string."""
        category = Category(name='Corporativo')
        assert str(category) == 'Corporativo'


@pytest.mark.django_db
class TestWork:
    """Testes para o modelo Work."""

    def test_create_work(self, videomaker_user):
        """Testa criação de trabalho."""
        work = Work.objects.create(
            videomaker=videomaker_user,
            title='Vídeo de Casamento',
            description='Um lindo vídeo de casamento',
            work_type='video',
        )
        assert work.title == 'Vídeo de Casamento'
        assert work.videomaker == videomaker_user
        assert work.status == 'draft'

    def test_work_str(self, videomaker_user):
        """Testa representação string."""
        work = Work(
            videomaker=videomaker_user,
            title='Clipe Musical',
        )
        assert str(work) == 'Clipe Musical - John Doe'

    def test_work_default_values(self, videomaker_user):
        """Testa valores padrão."""
        work = Work.objects.create(
            videomaker=videomaker_user,
            title='Teste',
            description='Descrição',
        )
        assert work.views_count == 0
        assert work.likes_count == 0
        assert work.status == 'draft'


@pytest.mark.django_db
class TestReview:
    """Testes para o modelo Review."""

    def test_create_review(self, user, videomaker_user):
        """Testa criação de avaliação."""
        review = Review.objects.create(
            reviewer=user,
            videomaker=videomaker_user,
            rating=5,
            comment='Excelente profissional!',
        )
        assert review.rating == 5
        assert review.reviewer == user

    def test_review_str(self, user, videomaker_user):
        """Testa representação string."""
        review = Review(
            reviewer=user,
            videomaker=videomaker_user,
            rating=4,
        )
        assert str(review) == 'Test User → John Doe (4★)'

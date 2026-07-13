# ===========================================
# FILMERSHUB - TESTES DE MODELOS (ACCOUNTS)
# ===========================================

import pytest
from django.contrib.auth import get_user_model
from apps.accounts.models import (
    VideomakerProfile,
    ClientProfile,
    Follow,
    Skill,
    VideomakerSkill,
)

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Testes para o modelo User customizado."""

    def test_create_user(self):
        """Testa criação de usuário."""
        user = User.objects.create_user(
            email='novo@test.com',
            password='senha123',
            first_name='João',
            last_name='Silva',
        )
        assert user.email == 'novo@test.com'
        assert user.first_name == 'João'
        assert user.is_active is True
        assert user.is_staff is False
        assert user.check_password('senha123')

    def test_create_superuser(self):
        """Testa criação de superusuário."""
        admin = User.objects.create_superuser(
            email='admin@test.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
        )
        assert admin.is_staff is True
        assert admin.is_superuser is True

    def test_user_str(self):
        """Testa representação string do usuário."""
        user = User(
            first_name='Maria',
            last_name='Santos',
        )
        assert str(user) == 'Maria Santos'

    def test_user_full_name(self):
        """Testa propriedade full_name."""
        user = User(
            first_name='Carlos',
            last_name='Oliveira',
        )
        assert user.full_name == 'Carlos Oliveira'

    def test_user_profile_type_both(self):
        """Testa profile_type 'both' ativa as duas flags."""
        user = User.objects.create_user(
            email='both@test.com',
            password='senha123',
            profile_type='both',
        )
        assert user.is_videomaker is True
        assert user.is_client is True

    def test_user_profile_type_videomaker(self):
        """Testa profile_type 'videomaker' ativa só videomaker."""
        user = User.objects.create_user(
            email='video@test.com',
            password='senha123',
            profile_type='videomaker',
        )
        assert user.is_videomaker is True
        assert user.is_client is False

    def test_user_profile_type_client(self):
        """Testa profile_type 'client' ativa só client."""
        user = User.objects.create_user(
            email='client@test.com',
            password='senha123',
            profile_type='client',
        )
        assert user.is_videomaker is False
        assert user.is_client is True

    def test_user_email_unique(self):
        """Testa que email é único."""
        User.objects.create_user(
            email='unique@test.com',
            password='senha123',
        )
        with pytest.raises(Exception):
            User.objects.create_user(
                email='unique@test.com',
                password='outra123',
            )

    def test_user_username_field(self):
        """Testa que USERNAME_FIELD é email."""
        assert User.USERNAME_FIELD == 'email'

    def test_user_required_fields(self):
        """Testa campos obrigatórios."""
        assert 'first_name' in User.REQUIRED_FIELDS
        assert 'last_name' in User.REQUIRED_FIELDS


@pytest.mark.django_db
class TestVideomakerProfile:
    """Testes para o modelo VideomakerProfile."""

    def test_create_videomaker_profile(self, videomaker_user):
        """Testa criação de perfil de videomaker."""
        profile = VideomakerProfile.objects.create(
            user=videomaker_user,
            specialty='wedding',
            hourly_rate=150.00,
            day_rate=800.00,
        )
        assert profile.user == videomaker_user
        assert profile.specialty == 'wedding'
        assert profile.hourly_rate == 150.00

    def test_videomaker_profile_str(self, videomaker_user):
        """Testa representação string."""
        profile = VideomakerProfile(user=videomaker_user)
        assert str(profile) == 'Videomaker: John Doe'

    def test_videomaker_default_values(self, videomaker_user):
        """Testa valores padrão."""
        profile = VideomakerProfile.objects.create(user=videomaker_user)
        assert profile.is_available is True
        assert profile.total_jobs == 0
        assert profile.average_rating == 0.0


@pytest.mark.django_db
class TestClientProfile:
    """Testes para o modelo ClientProfile."""

    def test_create_client_profile(self, client_user):
        """Testa criação de perfil de cliente."""
        profile = ClientProfile.objects.create(
            user=client_user,
            client_type='company',
            company_name='Empresa XYZ',
        )
        assert profile.user == client_user
        assert profile.client_type == 'company'

    def test_client_profile_str(self, client_user):
        """Testa representação string."""
        profile = ClientProfile(user=client_user)
        assert str(profile) == 'Cliente: Jane Smith'


@pytest.mark.django_db
class TestFollow:
    """Testes para o modelo Follow."""

    def test_create_follow(self, user, videomaker_user):
        """Testa criação de seguidor."""
        follow = Follow.objects.create(
            follower=user,
            followed=videomaker_user,
        )
        assert follow.follower == user
        assert follow.followed == videomaker_user

    def test_follow_str(self, user, videomaker_user):
        """Testa representação string."""
        follow = Follow(follower=user, followed=videomaker_user)
        assert str(follow) == 'Test User segue John Doe'

    def test_cannot_follow_self(self, user):
        """Testa que não pode seguir a si mesmo."""
        with pytest.raises(ValueError):
            Follow.objects.create(
                follower=user,
                followed=user,
            )

    def test_unique_follow(self, user, videomaker_user):
        """Testa que não pode seguir a mesma pessoa duas vezes."""
        Follow.objects.create(follower=user, followed=videomaker_user)
        with pytest.raises(Exception):
            Follow.objects.create(follower=user, followed=videomaker_user)


@pytest.mark.django_db
class TestSkill:
    """Testes para o modelo Skill."""

    def test_create_skill(self):
        """Testa criação de habilidade."""
        skill = Skill.objects.create(
            name='Edição de Vídeo',
            slug='edicao-video',
        )
        assert skill.name == 'Edição de Vídeo'

    def test_skill_str(self):
        """Testa representação string."""
        skill = Skill(name='Cinegrafismo')
        assert str(skill) == 'Cinegrafismo'


@pytest.mark.django_db
class TestVideomakerSkill:
    """Testes para o modelo VideomakerSkill."""

    def test_create_videomaker_skill(self, videomaker_user):
        """Testa criação de habilidade de videomaker."""
        profile = VideomakerProfile.objects.create(user=videomaker_user)
        skill = Skill.objects.create(name='Color Grading', slug='color-grading')
        vs = VideomakerSkill.objects.create(
            videomaker=profile,
            skill=skill,
            experience_level=4,
        )
        assert vs.experience_level == 4

    def test_videomaker_skill_str(self, videomaker_user):
        """Testa representação string."""
        profile = VideomakerProfile.objects.create(user=videomaker_user)
        skill = Skill.objects.create(name='Drone', slug='drone')
        vs = VideomakerSkill(videomaker=profile, skill=skill)
        assert str(vs) == 'Drone - John Doe'

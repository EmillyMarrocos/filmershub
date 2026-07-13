# ===========================================
# FILMERSHUB - VIEWS DE USUÁRIO
# ===========================================

from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import VideomakerProfile, ClientProfile, Follow, Skill
from .serializers import (
    UserSerializer,
    UserListSerializer,
    PublicProfileSerializer,
    VideomakerProfileSerializer,
    VideomakerProfileCreateUpdateSerializer,
    ClientProfileSerializer,
    ClientProfileCreateUpdateSerializer,
    FollowSerializer,
    SkillSerializer,
)

User = get_user_model()


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Perfil do usuário logado.

    GET /api/v1/profile/
    PUT /api/v1/profile/
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ProfileDeleteView(APIView):
    """
    Excluir conta do usuário logado.

    DELETE /api/v1/profile/delete/
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save(update_fields=['is_active'])
        return Response({'detail': 'Conta desativada com sucesso.'})


class PublicProfileView(generics.RetrieveAPIView):
    """
    Perfil público de um usuário.
    Esconde dados sensíveis (email, phone).

    GET /api/v1/users/<uuid:id>/
    """
    queryset = User.objects.all()
    serializer_class = PublicProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'


class VideomakerListView(generics.ListAPIView):
    """
    Lista de videomakers.

    GET /api/v1/videomakers/
    """
    queryset = User.objects.filter(
        is_videomaker=True,
        is_active=True
    )
    serializer_class = UserListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'city']
    ordering_fields = ['date_joined', 'first_name']


class VideomakerProfileView(generics.RetrieveUpdateAPIView):
    """
    Perfil de videomaker do usuário logado.

    GET /api/v1/videomaker-profile/
    PUT /api/v1/videomaker-profile/
    """
    serializer_class = VideomakerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = VideomakerProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return VideomakerProfileCreateUpdateSerializer
        return VideomakerProfileSerializer


class ClientProfileView(generics.RetrieveUpdateAPIView):
    """
    Perfil de cliente do usuário logado.

    GET /api/v1/client-profile/
    PUT /api/v1/client-profile/
    """
    serializer_class = ClientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = ClientProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ClientProfileCreateUpdateSerializer
        return ClientProfileSerializer


class FollowToggleView(APIView):
    """
    Seguir/deixar de seguir um usuário.

    POST /api/v1/users/<uuid:id>/follow/
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        """Toggle seguir/deixar de seguir."""
        user_to_follow = get_object_or_404(User, id=id)

        if user_to_follow == request.user:
            return Response(
                {'detail': 'Você não pode seguir a si mesmo.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            followed=user_to_follow
        )

        if not created:
            follow.delete()
            return Response(
                {'detail': 'Deixou de seguir.'},
                status=status.HTTP_200_OK
            )

        from apps.notifications.models import Notification
        Notification.objects.create(
            recipient=user_to_follow,
            sender=request.user,
            notification_type='follow',
            title='Novo seguidor',
            message=f'{request.user.full_name} começou a te seguir.',
            link=f'/profile/{request.user.id}',
        )

        return Response(
            {'detail': 'Agora você segue este usuário.'},
            status=status.HTTP_201_CREATED
        )


class FollowersListView(generics.ListAPIView):
    """
    Lista de seguidores de um usuário.

    GET /api/v1/users/<uuid:id>/followers/
    """
    serializer_class = FollowSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['id']
        return Follow.objects.filter(followed_id=user_id)


class FollowingListView(generics.ListAPIView):
    """
    Lista de usuários que um usuário segue.

    GET /api/v1/users/<uuid:id>/following/
    """
    serializer_class = FollowSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['id']
        return Follow.objects.filter(follower_id=user_id)


class SkillListView(generics.ListAPIView):
    """
    Lista de habilidades disponíveis.

    GET /api/v1/skills/
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class UserLookupView(APIView):
    """
    Busca usuário por email.

    GET /api/v1/users/lookup/?email=xxx
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        email = request.query_params.get('email', '').strip()
        if not email:
            return Response(
                {'detail': 'Parâmetro "email" é obrigatório.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.filter(email__iexact=email, is_active=True).first()
        if not user:
            return Response(
                {'detail': 'Usuário não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response({
            'id': str(user.id),
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': user.full_name,
            'avatar_url': None,
        })

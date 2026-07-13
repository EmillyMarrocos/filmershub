# ===========================================
# FILMERSHUB - VIEWS DE AUTENTICAÇÃO
# ===========================================

from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .serializers_auth import (
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    Registro de novo usuário.

    POST /api/v1/auth/register/
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """Registra usuário e retorna tokens JWT."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Gera tokens JWT
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': {
                'id': str(user.id),
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'full_name': user.full_name,
                'profile_type': user.profile_type,
                'is_videomaker': user.is_videomaker,
                'is_client': user.is_client,
                'avatar_url': None,
                'phone': user.phone,
                'bio': user.bio,
                'city': user.city,
                'state': user.state,
                'instagram': user.instagram,
                'youtube': user.youtube,
                'website': user.website,
                'date_joined': user.date_joined.isoformat(),
            },
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer customizado para login com JWT."""

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': str(self.user.id),
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'full_name': self.user.full_name,
            'profile_type': self.user.profile_type,
            'is_videomaker': self.user.is_videomaker,
            'is_client': self.user.is_client,
            'avatar_url': None,
            'phone': self.user.phone,
            'bio': self.user.bio,
            'city': self.user.city,
            'state': self.user.state,
            'instagram': self.user.instagram,
            'youtube': self.user.youtube,
            'website': self.user.website,
            'date_joined': self.user.date_joined.isoformat(),
        }
        return data


class LoginView(TokenObtainPairView):
    """
    Login com JWT.

    POST /api/v1/auth/login/
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]


class LogoutView(APIView):
    """
    Logout (revoga refresh token).

    POST /api/v1/auth/logout/
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Revoga o refresh token."""
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response(
                {'detail': 'Logout realizado com sucesso.'},
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {'detail': 'Erro ao realizar logout.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordView(generics.UpdateAPIView):
    """
    Alteração de senha.

    PUT /api/v1/auth/change-password/
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'detail': 'Senha alterada com sucesso.'},
            status=status.HTTP_200_OK
        )


class ForgotPasswordView(generics.GenericAPIView):
    """
    Solicita redefinição de senha.

    POST /api/v1/auth/forgot-password/
    """
    serializer_class = ForgotPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        if result['token']:
            return Response(
                {'detail': 'Email de redefinição enviado.', 'token': result['token']},
                status=status.HTTP_200_OK
            )
        return Response(
            {'detail': 'Email de redefinição enviado.'},
            status=status.HTTP_200_OK
        )


class ResetPasswordView(generics.GenericAPIView):
    """
    Redefine a senha com token.

    POST /api/v1/auth/reset-password/
    """
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'detail': 'Senha redefinida com sucesso.'},
            status=status.HTTP_200_OK
        )

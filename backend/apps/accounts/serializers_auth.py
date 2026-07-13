# ===========================================
# FILMERSHUB - SERIALIZERS DE AUTENTICAÇÃO
# ===========================================

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
import secrets
import datetime

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer para registro de novo usuário."""

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )

    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name',
            'password', 'password_confirm',
            'profile_type',
        ]

    def validate(self, attrs):
        """Valida senhas e dados."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'As senhas não conferem.'
            })
        return attrs

    def create(self, validated_data):
        """Cria novo usuário."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer para login."""

    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """Valida credenciais."""
        from django.contrib.auth import authenticate

        user = authenticate(
            email=attrs['email'],
            password=attrs['password']
        )

        if not user:
            raise serializers.ValidationError('Email ou senha inválidos.')

        if not user.is_active:
            raise serializers.ValidationError('Conta desativada.')

        attrs['user'] = user
        return attrs


class TokenSerializer(serializers.Serializer):
    """Serializer para tokens JWT."""

    access = serializers.CharField()
    refresh = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        """Retorna dados do usuário."""
        user = self.context.get('user')
        if user:
            return UserSerializer(user).data
        return None


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para alteração de senha."""

    old_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )

    new_password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate_old_password(self, value):
        """Valida senha atual."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Senha atual incorreta.')
        return value

    def validate(self, attrs):
        """Valida novas senhas."""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': 'As senhas não conferem.'
            })
        return attrs

    def save(self, **kwargs):
        """Salva nova senha."""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    """Serializer para solicitação de redefinição de senha."""
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            pass
        return value

    def save(self):
        email = self.validated_data['email']
        try:
            user = User.objects.get(email=email)
            token = secrets.token_urlsafe(32)
            expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
            user._reset_token = token
            user._reset_expires = expires
            user.save(update_fields=[])
            return {'token': token, 'email': email}
        except User.DoesNotExist:
            return {'token': None, 'email': email}


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer para redefinição de senha."""
    token = serializers.CharField()
    email = serializers.EmailField()
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': 'As senhas não conferem.'
            })
        return attrs

    def save(self):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError('Usuário não encontrado.')

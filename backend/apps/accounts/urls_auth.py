# ===========================================
# FILMERSHUB - URLS DE AUTENTICAÇÃO
# ===========================================

from django.urls import path
from . import views_auth

urlpatterns = [
    # Registro
    path('register/', views_auth.RegisterView.as_view(), name='register'),

    # Login
    path('login/', views_auth.LoginView.as_view(), name='token_obtain_pair'),

    # Logout
    path('logout/', views_auth.LogoutView.as_view(), name='logout'),

    # Alterar senha
    path('change-password/', views_auth.ChangePasswordView.as_view(), name='change-password'),

    # Esqueci a senha
    path('forgot-password/', views_auth.ForgotPasswordView.as_view(), name='forgot-password'),

    # Redefinir senha
    path('reset-password/', views_auth.ResetPasswordView.as_view(), name='reset-password'),
]

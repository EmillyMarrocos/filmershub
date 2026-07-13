# ===========================================
# FILMERSHUB - URLS PRINCIPAIS
# ===========================================
# Arquivo raiz de URLs do Django
# Todas as URLs da API começam aqui

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# ===========================================
# URLS DA API
# ===========================================

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API v1
    path('api/v1/', include([
        # Auth (login, registro, refresh token)
        path('auth/', include('apps.accounts.urls_auth')),

        # Perfis de usuário
        path('', include('apps.accounts.urls')),

        # Portfólio
        path('portfolio/', include('apps.portfolio.urls')),

        # Feed social
        path('feed/', include('apps.feed.urls')),

        # Chat
        path('chat/', include('apps.chat.urls')),

        # Agendamento
        path('scheduling/', include('apps.scheduling.urls')),

        # Contratos
        path('contracts/', include('apps.contracts.urls')),

        # Pagamentos
        path('payments/', include('apps.payments.urls')),

        # Notificações
        path('notifications/', include('apps.notifications.urls')),

        # Landing page
        path('landing/', include('apps.landing.urls')),
    ])),

    # Documentação da API (Swagger/ReDoc)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# ===========================================
# ARQUIVOS MÍDIA (uploads) - só em desenvolvimento
# ===========================================

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

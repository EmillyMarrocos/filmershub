# ===========================================
# FILMERSHUB - CONFIGURAÇÕES BASE
# ===========================================
# Configurações compartilhadas entre todos os ambientes
# Cada ambiente (dev, prod) herda deste arquivo

import os
from pathlib import Path
from datetime import timedelta
from decouple import config

# ===========================================
# CAMINHOS DO PROJETO
# ===========================================

# Base directory (backend/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ===========================================
# SEGURANÇA
# ===========================================

# Chave secreta do Django (gerada em produção)
SECRET_KEY = config('DJANGO_SECRET_KEY', default='django-insecure-change-me-in-production')

# Modo debug (True em dev, False em produção)
DEBUG = config('DJANGO_DEBUG', default=True, cast=bool)

# Hosts permitidos
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# ===========================================
# APPS INSTALADOS
# ===========================================

INSTALLED_APPS = [
    # Django defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular',
    'corsheaders',
    'channels',

    # Local apps
    'apps.accounts',
    'apps.portfolio',
    'apps.feed',
    'apps.chat',
    'apps.scheduling',
    'apps.contracts',
    'apps.payments',
    'apps.notifications',
]

# ===========================================
# MIDDLEWARE
# ===========================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS deve vir antes do CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ===========================================
# URLS
# ===========================================

ROOT_URLCONF = 'config.urls'

# ===========================================
# TEMPLATES
# ===========================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ===========================================
# WSGI / ASGI
# ===========================================

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# ===========================================
# BANCO DE DADOS
# ===========================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_URL', default='filmershub').split('/')[-1] if 'DATABASE_URL' in os.environ else 'filmershub',
        'USER': config('DATABASE_URL', default='postgres://filmershub:filmershub@localhost:5432/filmershub').split('//')[1].split(':')[0] if 'DATABASE_URL' in os.environ else 'filmershub',
        'PASSWORD': config('DATABASE_URL', default='postgres://filmershub:filmershub@localhost:5432/filmershub').split(':')[2].split('@')[0] if 'DATABASE_URL' in os.environ else 'filmershub',
        'HOST': config('DATABASE_URL', default='postgres://filmershub:filmershub@localhost:5432/filmershub').split('@')[1].split(':')[0] if 'DATABASE_URL' in os.environ else 'localhost',
        'PORT': config('DATABASE_URL', default='postgres://filmershub:filmershub@localhost:5432/filmershub').split(':')[-1].split('/')[0] if 'DATABASE_URL' in os.environ else '5432',
    }
}

# ===========================================
# REDIS (CACHE + CHANNELS)
# ===========================================

REDIS_URL = config('REDIS_URL', default='redis://localhost:6379/0')

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
    }
}

# Channel Layers (WebSocket)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(REDIS_URL.split('://')[1].split(':')[0], int(REDIS_URL.split(':')[-1].split('/')[0]))],
        },
    },
}

# ===========================================
# VALIDAÇÃO DE SENHA
# ===========================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ===========================================
# INTERNACIONALIZAÇÃO
# ===========================================

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ===========================================
# ARQUIVOS ESTÁTICOS
# ===========================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ===========================================
# ARQUIVOS MÍDIA (UPLOADS)
# ===========================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ===========================================
# MODEL DEFAULT
# ===========================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===========================================
# USER MODEL CUSTOMIZADO
# ===========================================

AUTH_USER_MODEL = 'accounts.User'

# ===========================================
# DJANGO REST FRAMEWORK
# ===========================================

REST_FRAMEWORK = {
    # Autenticação padrão: JWT
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    # Permissão padrão: autenticado
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    # Paginação
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,

    # Schema (Swagger)
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    # Filtros
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# ===========================================
# SIMPLE JWT
# ===========================================

SIMPLE_JWT = {
    # Tempo de vida do access token
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=config('JWT_ACCESS_TOKEN_LIFETIME', default=30, cast=int)),

    # Tempo de vida do refresh token
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=config('JWT_REFRESH_TOKEN_LIFETIME', default=10080, cast=int)),

    # Algoritmo de assinatura
    'ALGORITHM': 'HS256',

    # Chave secreta (usa a mesma do Django)
    'SIGNING_KEY': SECRET_KEY,

    # Permite refresh de token
    'ROTATE_REFRESH_TOKENS': True,

    # Blacklist de tokens revogados
    'BLACKLIST_AFTER_ROTATION': True,
}

# ===========================================
# CORS (Cross-Origin Resource Sharing)
# ===========================================

CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:5173',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# Permite credenciais (cookies, headers de auth)
CORS_ALLOW_CREDENTIALS = True

# ===========================================
# DRF SPECTACULAR (SWAGGER)
# ===========================================

SPECTACULAR_SETTINGS = {
    'TITLE': 'FilmersHub API',
    'DESCRIPTION': 'API da plataforma FilmersHub para videomakers',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'TAGS': [
        {'name': 'auth', 'description': 'Autenticação e perfis'},
        {'name': 'portfolio', 'description': 'Portfólio de trabalhos'},
        {'name': 'feed', 'description': 'Feed social'},
        {'name': 'chat', 'description': 'Chat em tempo real'},
        {'name': 'scheduling', 'description': 'Agendamento'},
        {'name': 'contracts', 'description': 'Contratos'},
        {'name': 'payments', 'description': 'Pagamentos'},
        {'name': 'notifications', 'description': 'Notificações'},
    ],
}

# ===========================================
# LOGGING
# ===========================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

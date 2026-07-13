# ===========================================
# FILMERSHUB - CONFIGURAÇÕES DE TESTE
# ===========================================
# Usa SQLite para testes (não precisa de Docker/PostgreSQL)

from .base import *  # noqa: F401,F403

# ===========================================
# DEBUG
# ===========================================

DEBUG = False

# ===========================================
# BANCO DE DADOS (SQLite para testes)
# ===========================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# ===========================================
# CACHE (in-memory para testes)
# ===========================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# ===========================================
# CHANNELS (in-memory para testes)
# ===========================================

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# ===========================================
# EMAIL (console para testes)
# ===========================================

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# ===========================================
# PASSWORD HASHERS (mais rápido para testes)
# ===========================================

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# ===========================================
# SEGURANÇA
# ===========================================

SECRET_KEY = 'test-secret-key-not-for-production'
ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True

# ===========================================
# ARQUIVOS ESTÁTICOS
# ===========================================

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

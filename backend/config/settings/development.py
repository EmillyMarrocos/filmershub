# ===========================================
# FILMERSHUB - CONFIGURAÇÕES DE DESENVOLVIMENTO
# ===========================================
# Usado quando: python manage.py runserver

from .base import *  # noqa: F401,F403

# ===========================================
# DEBUG
# ===========================================

DEBUG = True

# ===========================================
# BANCO DE DADOS (SQLite para dev rápido)
# ===========================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ===========================================
# CACHE (LocalMemory para dev sem Redis)
# ===========================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Channel Layers (In-memory para dev sem Redis)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    }
}

# ===========================================
# CORS (permite frontend em outra porta)
# ===========================================

CORS_ALLOW_ALL_ORIGINS = True

# ===========================================
# EMAIL (console para dev)
# ===========================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Emails aparecem no terminal do Django

# ===========================================
# DJANGO DEBUG TOOLBAR (instalar: pip install django-debug-toolbar)
# ===========================================

# INSTALLED_APPS += ['debug_toolbar']  # noqa: F405
# MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')  # noqa: F405
# INTERNAL_IPS = ['127.0.0.1', 'localhost']

# ===========================================
# DJANGO EXTENSIONS
# ===========================================

# Shell Plus: mostra todos os models ao abrir o shell
# SHELLENVIRONS_DEFAULT_EXTENSIONS = [
#     'django_extensions.management.shell.ShellPlus'
# ]

# ===========================================
# LOGGING DETALHADO
# ===========================================

LOGGING['handlers']['file'] = {  # noqa: F405
    'class': 'logging.FileHandler',
    'filename': BASE_DIR / 'logs' / 'django.log',  # noqa: F405
    'formatter': 'verbose',
}

LOGGING['loggers']['django']['handlers'].append('file')  # noqa: F405

# Cria pasta de logs se não existir
import os
os.makedirs(BASE_DIR / 'logs', exist_ok=True)  # noqa: F405

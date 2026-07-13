# ===========================================
# FILMERSHUB - CONFIGURAÇÕES DE PRODUÇÃO
# ===========================================
# Usado quando: gunicorn config.wsgi:application

from .base import *  # noqa: F401,F403

# ===========================================
# DEBUG (SEMPRE False em produção!)
# ===========================================

DEBUG = False

# ===========================================
# SEGURANÇA
# ===========================================

# HTTPS
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookies seguros
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ===========================================
# BANCO DE DADOS (PostgreSQL em produção)
# ===========================================

# DATABASES já está configurado em base.py com PostgreSQL

# ===========================================
# EMAIL (SendGrid em produção)
# ===========================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = config('SENDGRID_API_KEY')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='FilmersHub <noreply@filmershub.com>')

# ===========================================
# CORS (só permite origens específicas)
# ===========================================

CORS_ALLOW_ALL_ORIGINS = False
# CORS_ALLOWED_ORIGINS já está em base.py

# ===========================================
# CORS (WebSocket)
# ===========================================

# Permite WebSocket em produção
ALLOWED_HOSTS += ['ws://*', 'wss://*']

# ===========================================
# STATIC FILES (Whitenoise)
# ===========================================

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')  # noqa: F405
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ===========================================
# SENTRY (monitoramento de erros)
# ===========================================

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=config('SENTRY_DSN', default=''),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=True,
)

# ===========================================
# CACHE REDIS
# ===========================================

# Cache já está configurado em base.py com Redis

# ===========================================
# GUNICORN
# ===========================================

# Configurações do Gunicorn
bind = '0.0.0.0:8000'
workers = 4
worker_class = 'uvicorn.workers.UvicornWorker'
timeout = 120
keepalive = 5

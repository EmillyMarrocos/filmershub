# ===========================================
# FILMERSHUB - WSGI
# ===========================================
# Ponto de entrada para HTTP normal (APIs REST)
# Executa com: gunicorn

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

# Inicializa o WSGI do Django
application = get_wsgi_application()

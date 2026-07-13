# ===========================================
# FILMERSHUB - ASGI
# ===========================================
# Ponto de entrada para WebSockets (chat, notificações)
# Executa com: daphne ou channels

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

# Inicializa o ASGI do Django
django_asgi_app = get_asgi_application()

# Importa as rotas WebSocket
from config.routing import websocket_urlpatterns  # noqa: E402

application = ProtocolTypeRouter({
    # HTTP normal (APIs REST)
    'http': django_asgi_app,

    # WebSocket (chat em tempo real)
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})

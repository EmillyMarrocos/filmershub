# ===========================================
# FILMERSHUB - ROTAS WEBSOCKET
# ===========================================
# URLs para WebSocket (chat em tempo real)
# Conexão: ws://localhost:8000/ws/chat/<sala>/

from django.urls import re_path
from apps.chat import consumers

websocket_urlpatterns = [
    # Chat: ws://localhost:8000/ws/chat/<sala_id>/
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

# ===========================================
# FILMERSHUB - CHAT WEBSOCKET CONSUMER
# ===========================================

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Consumer WebSocket para chat em tempo real.

    Conecta: ws://localhost:8000/ws/chat/<room_name>/
    """

    async def connect(self):
        """Conecta ao WebSocket."""
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Verifica se o usuário está autenticado
        if self.scope['user'].is_anonymous:
            await self.close()
            return

        # Entra no grupo da sala
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Envia mensagem de conexão
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Conectado ao chat!'
        }))

    async def disconnect(self, close_code):
        """Desconecta do WebSocket."""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Recebe mensagem do WebSocket."""
        try:
            data = json.loads(text_data)
            message_type = data.get('type', 'text')
            content = data.get('content', '')

            if content:
                # Salva a mensagem no banco
                message = await self.save_message(
                    message_type=message_type,
                    content=content
                )

                # Envia para o grupo
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': {
                            'id': str(message.id),
                            'sender': self.scope['user'].full_name,
                            'sender_id': str(self.scope['user'].id),
                            'content': content,
                            'message_type': message_type,
                            'created_at': message.created_at.isoformat(),
                        }
                    }
                )
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'JSON inválido'
            }))

    async def chat_message(self, event):
        """Recebe mensagem do grupo e envia ao WebSocket."""
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'message': event['message']
        }))

    @database_sync_to_async
    def save_message(self, message_type, content):
        """Salva a mensagem no banco de dados."""
        from .models import ChatRoom, Message

        room = ChatRoom.objects.get(id=self.room_name)
        return Message.objects.create(
            room=room,
            sender=self.scope['user'],
            content=content,
            message_type=message_type,
        )

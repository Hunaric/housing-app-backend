import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import ConversationMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat{self.room_name}'

        # Join room

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        

    async def disconnect(self):
        # Leave room

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    # Receive message from web socket
    async def receive(self, text_data):
        data = json.loads(text_data)

        body = data['data']['body']
        name = data['data']['name']
        sent_to_id = data['data']['sent_to_id']
        conversation_id = data['data']['conversation_id']

        # Récupérer l'utilisateur connecté
        user = self.scope.get('user')  

        if user is None or not user.is_authenticated:
            return  # Ignore si l'utilisateur n'est pas authentifié


        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'body': body,
                'created_by': {
                    'id': str(user.id),
                    'name': str(user.name) if not callable(user.name) else '',
                    'email': str(user.email) if not callable(user.email) else '',
                    'avatar_url': str(user.avatar_url) if hasattr(user, 'avatar_url') and not callable(user.avatar_url) else ''
                }
            }
        )

        await self.save_message(conversation_id, body, sent_to_id)


    # Sending message
    async def chat_message(self, event):
        body = event.get('body', '')
        created_by = event.get('created_by', {})


        # Vérification des types pour éviter l'erreur
        if not isinstance(created_by, dict):
            created_by = {}

        await self.send(text_data=json.dumps({
            'body': body,
            'created_by': {
            'id': str(created_by.get('id', '')),  
            'name': created_by.get('name', ''),  
            'email': created_by.get('email', ''),  
            'avatar_url': created_by.get('avatar_url', '')
            }  
        }))


    # Store and load message section
    @sync_to_async
    def save_message(self, conversation_id, body, send_to_id):
        user = self.scope['user']

        ConversationMessage.objects.create(conversation_id=conversation_id, body=body, sent_to_id=send_to_id, created_by=user)
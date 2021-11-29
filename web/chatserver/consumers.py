import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django_mongoengine.mongo_auth.models import User

from .models import Chatroom, chatmessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # print(dir(self.scope["session"]))
        # print(self.scope["session"].items())
        # print(self.scope["session"].get('username'))
        # print(self.scope["session"].get('is_login'))
        # print(self.scope)
        # print(dir(self.scope))
        # print(dir(self.scope['user']))
        # print(self.scope["user"].username)
        # print(self.scope["user"].is_authenticated)
        self.user = await self.get_name(self.scope["session"]["username"])

        self.scope["session"].save()

        # Join chatroom
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Save chatroom to DB if not present
        await self.save_room_to_db(self.room_group_name)

        # login user to chatroom (DB)
        await self.login_user_to_room(self.room_group_name, self.user[0].username)

        await self.accept()

        # Get past messages from chatroom and broadcase to everyone in the room
        pastmessages = await self.get_past_messages()

        for m in pastmessages:
            await self.send(text_data=json.dumps({
                'message': m.message,
                'username': m.username,
                'timestamp': str(m.timestamp)
            }))

    # When Client disconnects
    async def disconnect(self, close_code):
        # Leave chatroom
        await self.logout_user_from_room(self.room_group_name, self.user[0].username)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket|Client
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(f"message from client: {text_data_json}")
        message = text_data_json['message']
        fromuser = text_data_json['username']
        isodatetime = text_data_json['isodatetime']

        # Send message to chatroom
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'from': fromuser,
                'isodatetime': isodatetime
            }
        )

        # Write Message to DB
        await self.write_message_to_db(message, self.room_group_name, self.user[0].username, isodatetime)

    # Receive message from Chatroom
    async def chat_message(self, event):
        message = event['message']
        fromuser = event['from']

        # Send message to WebSocket|client
        await self.send(text_data=json.dumps({
            'message': message,
            'username': fromuser,
            'timestamp': str(datetime.datetime.now())
        }))

    @database_sync_to_async
    def get_name(self, username):
        return User.objects(username=username)

    @database_sync_to_async
    def save_room_to_db(self, chatroom):
        c = Chatroom.objects(chatroom=chatroom)
        if not c:
            croom = Chatroom()
            croom.chatroom = self.room_group_name
            croom.save()
        return

    @database_sync_to_async
    def login_user_to_room(self, chatroom, username):
        c = Chatroom.objects(chatroom=chatroom)
        c.update_one(push__users=username)
        return

    @database_sync_to_async
    def logout_user_from_room(self, chatroom, username):
        c = Chatroom.objects(chatroom=chatroom)
        c.update_one(pull__users=username)
        return

    @database_sync_to_async
    def write_message_to_db(self, message, chatroom, username, isodatetime):
        chat = chatmessage()
        chat.message = message
        chat.chatroom = chatroom
        chat.username = username
        chat.timestamp = datetime.datetime.strptime(isodatetime, '%Y-%m-%dT%H:%M:%S.%fZ')
        chat.save()
        return

    @database_sync_to_async
    def get_past_messages(self):
        messages = chatmessage.objects(chatroom=self.room_group_name).order_by("timestamp", "-1")
        return messages
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Chat, Contact, Message
from django.contrib.auth.models import User

from chat.views import get_last_10_messages


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        # get room messages
        # Get last 10 messages
        print("SCOPE", self.scope)
        messages = Chat.objects.filter(
            id=self.room_name,
            participants__in=[self.scope["user"]],
        )[0].messages.all()
        print("Messages:::", messages)

        content = {
            "command": "messages",
            "messages": self.messages_to_json(messages),
        }
        self.send_message(content)

    def new_message(self, data):
        author = data["from"]
        author_user = User.objects.filter(username=author)[0]
        print("Auth User", author_user)
        contact, _ = Contact.objects.get_or_create(
            user=author_user,
        )
        message = Message.objects.create(
            contact=contact,
            message=data["message"],
        )
        chat = Chat.objects.filter(
            id=self.room_name,
            participants__in=[self.scope["user"]],
        )[0]

        chat.messages.add(message)
        chat.save()

        content = {
            "command": "new_message",
            "message": self.message_to_json(message),
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            "author": message.contact.user.username,
            "content": message.message,
            "timestamp": str(message.created_at),
        }

    commands = {
        "fetch_messages": fetch_messages,
        "new_messages": new_message,
    }

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

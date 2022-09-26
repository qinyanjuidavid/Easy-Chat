import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from chat.models import Chat, Contact, Message
from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
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
            "read": message.is_read,
            "delivered": message.is_delivered,
            "seen": message.is_seen,
            "file": str(message.file),
            "id": message.id,
            "message_id": message.id,
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
        print("Data-->", data)
        self.commands[data["command"]](self, data)

    def send_chat_message(self, message):
        print("Chat message:::", message)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "chat_message", "message": message},
        )

    def send_message(self, message):
        print("Send message:::", message)
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        print("Event-->", event)

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

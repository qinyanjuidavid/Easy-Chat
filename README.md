# Chat

Recap on django channels

## Chat/Routing.py

- For the Chat/routing.py my code goes as follows

```
from django.urls import path
from chat import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi())
]
```

## Routing.py

- For the routing.py my code goes as follows

```
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

application = ProtocolTypeRouter({
   'websocket': AuthMiddlewareStack(
       URLRouter(
           chat.routing.websocket_urlpatterns
           )
         ),
       })
```

> The Django Channels does not include the routing.py in the root directory of the project but instead uses the code in the asgi

> Do not forget to add the code below in your settings.py, Channels can't be able to run in the wsgi protocol

```
ASGI_APPLICATION="src.routing.application"
```

> The asgi.py can remain the same as long as you have configured the root routing.py to point to the asgi.py

## The index template

> For my code i used a base.html, whereas, the django read the docs never used to that to keep the code dry

```
{%extends 'chat/base.html'%} {%block title%}{%endblock%} {%block style%}
{%endblock%} {%block content%}
What chat room would you like to enter?<br />
<input id="room-name-input" type="text" size="100" /><br />
<input id="room-name-submit" type="button" value="Enter" />

<script>
 document.querySelector("#room-name-input").focus();
 document.querySelector("#room-name-input").onkeyup = function (e) {
   if (e.keyCode === 13) {
     // enter, return
     document.querySelector("#room-name-submit").click();
   }
 };

 document.querySelector("#room-name-submit").onclick = function (e) {
   var roomName = document.querySelector("#room-name-input").value;
   window.location.pathname = "/chat/" + roomName + "/";
 };
</script>

{%endblock%} {%block javascript%} {%endblock%}

```

### The room template

> The Code in the room.html goes as follows...

```
{%extends 'chat/base.html'%}
{%block title%}
Chat Room
{%endblock%}
{%block style%}
{%endblock%}
{%block content%}
<textarea id="chat-log" cols="100" rows="20"></textarea><br>
   <input id="chat-message-input" type="text" size="100"><br>
   <input id="chat-message-submit" type="button" value="Send">
   {{ room_name|json_script:"room-name" }}
   <script>
       const roomName = JSON.parse(document.getElementById('room-name').textContent);

       const chatSocket = new WebSocket(
           'ws://'
           + window.location.host
           + '/ws/chat/'
           + roomName
           + '/'
       );

       chatSocket.onmessage = function(e) {
           const data = JSON.parse(e.data);
           document.querySelector('#chat-log').value += (data.message + '\n');
       };

       chatSocket.onclose = function(e) {
           console.error('Chat socket closed unexpectedly');
       };

       document.querySelector('#chat-message-input').focus();
       document.querySelector('#chat-message-input').onkeyup = function(e) {
           if (e.keyCode === 13) {  // enter, return
               document.querySelector('#chat-message-submit').click();
           }
       };

       document.querySelector('#chat-message-submit').onclick = function(e) {
           const messageInputDom = document.querySelector('#chat-message-input');
           const message = messageInputDom.value;
           chatSocket.send(JSON.stringify({
               'message': message
           }));
           messageInputDom.value = '';
       };
   </script>
{%endblock%}
{%block javascript%}

{%endblock%}
```

## Models.py

- Created my models as follows;

```
class Message(models.Model):
   author = models.ForeignKey(
       User, related_name="author_messages", on_delete=models.CASCADE)
   content = models.TextField()
   timestamp = models.DateTimeField(auto_now_add=True)

   def __str__(self):
       return str(self.author.username)

   def last_10_messages(self):
       return Message.objects.order_by('-timestamp').all()[:10]

```

## Consumer.py

- The basic code for the consumer goes as follows:

```
import json
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
  def connect(self):
      self.accept()

  def disconnect(self, close_code):
      pass

  def receive(self, text_data):
      text_data_json = json.loads(text_data)
      message = text_data_json['message']
      self.send(text_data=json.dumps({
          'message': message
      }))
```

## Enabling the channel layer

- In order for us to enable the channel layer we will use redis to store our messages. In this case we will install redis using the docker To install redis using docker we will type this command in our terminal;

> docker pull redis

- To start the redis port on our terminal we will run this command;

> docker run -p 6379:6379 -d redis:5

- The next step will be to install the channels_redis in our project to do that we will use pip for this case,

> python -m pip install channels_redis

- Basic a channels layer is what enables our chat application to send messages to the clients in the room, the channels layer is usually configured in the settings.py and the code goes as follows;

```
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```

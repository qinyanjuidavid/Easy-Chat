# Chat
Recap on django channels

## Chat/Routing.py
 - For the Chat/routing.py my code goes as follows
 
 ```
 from django.urls import path
 from chat import consumers

 websocket_urlpatterns = [
     path('ws/chat/<room_name>/', consumers.ChatConsumer.as_asgi())
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
 ASGI_APPLICATION="src.asgi.application"
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

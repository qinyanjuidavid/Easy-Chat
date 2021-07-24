# Chat
Recap on django channels
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

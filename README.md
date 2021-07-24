# Chat
Recap on django channels

    - Channels Read the doc does not include the routings.py in the projects root folder but instead includes it in the asgi, Quite a missed understanding

    - For the routing.py my code goes as follows 
    ```
    Python
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
from channels.auth import AuthMiddlewareStack
# to add auth in the chat app or getting the user
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import app.routing

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        # wrapp it in AuthMiddlewareStack to add authentication
        URLRouter(
            app.routing.websocket_urlpatterns
        )
    ),
})

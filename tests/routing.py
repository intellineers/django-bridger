from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from bridger.websockets.auth import JWTAuthMiddlewareStack
from bridger.websockets.consumers import AsyncAuthenticatedJsonWebsocketConsumer

websocket_urlpatterns = [path("ws/socket/", AsyncAuthenticatedJsonWebsocketConsumer)]

application = ProtocolTypeRouter(
    {"websocket": JWTAuthMiddlewareStack(URLRouter(websocket_urlpatterns))}
)

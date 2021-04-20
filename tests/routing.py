from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from channels.routing import URLRouter
from django.urls import path

from bridger.notifications.consumers import NotificationConsumer
from bridger.websockets.auth import JWTAuthMiddlewareStack
from bridger.websockets.consumers import AsyncAuthenticatedJsonWebsocketConsumer

websocket_urlpatterns = [
    path("ws/socket/", AsyncAuthenticatedJsonWebsocketConsumer),
    path("ws/notification/", NotificationConsumer),
]

application = ProtocolTypeRouter(
    {"websocket": JWTAuthMiddlewareStack(URLRouter(websocket_urlpatterns))}
)
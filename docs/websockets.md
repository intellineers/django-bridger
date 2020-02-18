The bridger provides an interface for websockets through django-channels with the addition of a jwt-authentication.

### Setup Websockets

1. Make sure `bridger` is installed with all needed dependencies and added to the `INSTALLED_APPS` in `settings.py`
    1. `channels`
    2. `djangorestframework-simplejwt`
2. Setup a `CHANNEL_LAYER` and the `JWT_AUTH_COOKIE`
3. Create a `routing.py` and add the `ASGI_APPLICATION` in `settings.py`

```python
# project.settings.py
INSTALLED_APPS = [
    ...
    "bridger",
    "channels",
    ...
]
CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
JWT_AUTH = {"JWT_AUTH_COOKIE": "JWT"}
ASGI_APPLICATION = project.routing.application

# project.routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from bridger.websockets.auth import JWTAuthMiddlewareStack

application = ProtocolTypeRouter(
    {"websocket": JWTAuthMiddlewareStack(URLRouter(urlpatterns))}
)
```
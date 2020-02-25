import json

import pytest
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from bridger.notifications.consumers import NotificationConsumer
from bridger.websockets.auth import JWTAuthMiddlewareStack


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_notification():
    user = get_user_model().objects.create(
        username="test_user", password="ABC", is_active=True, is_superuser=True
    )
    jwt_token = str(RefreshToken.for_user(user).access_token)

    headers = [(b"cookie", f"JWT-access={jwt_token}".encode())]
    communicator = WebsocketCommunicator(
        JWTAuthMiddlewareStack(NotificationConsumer), "/test/", headers=headers,
    )
    connected, subprotocol = await communicator.connect()

    assert connected

    payload = {"some": "data"}

    await get_channel_layer().group_send(
        f"notification-{user.id}", {"content": payload, "type": "notification.notify"},
    )
    response = await communicator.receive_from()
    assert json.loads(response) == payload

    await communicator.disconnect()

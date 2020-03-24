import json

import pytest
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from rest_framework_simplejwt.tokens import RefreshToken

from bridger.notifications.consumers import NotificationConsumer
from bridger.notifications.models import (
    Notification,
    NotificationSendType,
    post_create_notification,
)
from bridger.websockets.auth import JWTAuthMiddlewareStack


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_notification():
    post_save.disconnect(receiver=post_create_notification, sender=Notification)
    user = get_user_model().objects.create(
        username="test_user", password="ABC", is_active=True, is_superuser=True
    )
    notification = Notification.objects.create(
        recipient=user,
        title="New Notification",
        message="You have a new notification",
        send_type=NotificationSendType.MAIL.value,
    )

    jwt_token = str(RefreshToken.for_user(user).access_token)

    headers = [(b"cookie", f"JWT-access={jwt_token}".encode())]
    communicator = WebsocketCommunicator(
        JWTAuthMiddlewareStack(NotificationConsumer), "/test/", headers=headers,
    )
    connected, subprotocol = await communicator.connect()

    assert connected

    await get_channel_layer().group_send(
        f"notification-{user.id}",
        {"notification_id": notification.id, "type": "notification.notify"},
    )
    response = await communicator.receive_from()
    assert json.loads(response) == notification.to_payload()

    await communicator.disconnect()
    post_save.connect(receiver=post_create_notification, sender=Notification)

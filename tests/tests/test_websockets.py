import pytest
from channels.testing import WebsocketCommunicator

from bridger.websockets.auth import JWTAuthMiddlewareStack
from bridger.websockets.consumers import AsyncAuthenticatedJsonWebsocketConsumer


@pytest.mark.asyncio
async def test_connect_failed():
    communicator = WebsocketCommunicator(
        AsyncAuthenticatedJsonWebsocketConsumer, "/test/"
    )
    connected, subprotocol = await communicator.connect()

    assert not connected
    await communicator.disconnect()


@pytest.mark.asyncio
async def test_connect():
    headers = [(b"cookie", {"a": "b"})]

    # jwt = JWTAuthMiddlewareStack()(scope=headers)
    # print(jwt)

    communicator = WebsocketCommunicator(
        JWTAuthMiddlewareStack(AsyncAuthenticatedJsonWebsocketConsumer),
        "/test/",
        headers=headers,
    )
    connected, subprotocol = await communicator.connect()

    assert not connected
    await communicator.disconnect()
    assert False

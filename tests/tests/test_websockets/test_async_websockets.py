# import pytest
# from channels.testing import WebsocketCommunicator
# from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.tokens import RefreshToken

# from bridger.websockets.auth import JWTAuthMiddlewareStack
# from bridger.websockets.consumers import AsyncAuthenticatedJsonWebsocketConsumer


# @pytest.mark.asyncio
# async def test_connect_failed_no_cookie():
#     communicator = WebsocketCommunicator(
#         AsyncAuthenticatedJsonWebsocketConsumer, "/test/"
#     )
#     connected, subprotocol = await communicator.connect()

#     assert not connected
#     await communicator.disconnect()


# @pytest.mark.asyncio
# async def test_connect_failed_wrong_token():
#     headers = [(b"cookie", b"JWT-access=This.is.the.wrong.token")]

#     communicator = WebsocketCommunicator(
#         JWTAuthMiddlewareStack(AsyncAuthenticatedJsonWebsocketConsumer),
#         "/test/",
#         headers=headers,
#     )
#     connected, subprotocol = await communicator.connect()

#     assert not connected
#     await communicator.disconnect()


# @pytest.mark.asyncio
# @pytest.mark.django_db
# async def test_connect():
#     user = get_user_model().objects.create(
#         username="test_user", password="ABC", is_active=True, is_superuser=True
#     )
#     jwt_token = str(RefreshToken.for_user(user).access_token)

#     headers = [(b"cookie", f"JWT-access={jwt_token}".encode())]
#     communicator = WebsocketCommunicator(
#         JWTAuthMiddlewareStack(AsyncAuthenticatedJsonWebsocketConsumer),
#         "/test/",
#         headers=headers,
#     )
#     connected, subprotocol = await communicator.connect()

#     assert connected
#     await communicator.disconnect()

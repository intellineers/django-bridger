from channels.generic.websocket import (AsyncJsonWebsocketConsumer,
                                        JsonWebsocketConsumer)


class AsyncAuthenticatedConsumerMixin:
    async def connect(self):
        user = self.scope.get("user", None)
        if user is not None:
            await self.accept()
        else:
            await self.close()


class AuthenticatedConsumerMixin:
    def connect(self):
        user = self.scope.get("user", None)
        if user is not None:
            return self.accept()
        return self.close()


class AsyncAuthenticatedJsonWebsocketConsumer(
    AuthenticatedConsumerMixin, AsyncJsonWebsocketConsumer
):
    pass


class AuthenticatedJsonWebsocketConsumer(
    AuthenticatedConsumerMixin, JsonWebsocketConsumer
):
    pass

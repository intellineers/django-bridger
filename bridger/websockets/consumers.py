from channels.generic.websocket import AsyncJsonWebsocketConsumer, JsonWebsocketConsumer


class AsyncAuthenticatedConsumerMixin:
    async def connect(self):
        user = self.scope.get("user", None)
        if user is not None:
            await self.accept()
        else:
            await self.close()


class AsyncAuthenticatedJsonWebsocketConsumer(AsyncAuthenticatedConsumerMixin, AsyncJsonWebsocketConsumer):
    pass

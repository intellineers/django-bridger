from bridger.websockets.consumers import AsyncAuthenticatedJsonWebsocketConsumer

from .models import Notification


class NotificationConsumer(AsyncAuthenticatedJsonWebsocketConsumer):
    async def connect(self):
        await super().connect()
        if "user" in self.scope:
            channel_layer_name = f"notification-{self.scope['user'].id}"
            await self.channel_layer.group_add(channel_layer_name, self.channel_name)

    async def notification_notify(self, content):
        await self.send_json(
            Notification.objects.get(id=content["notification_id"]).to_payload()
        )

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.utils import timezone

from bridger.websockets.consumers import AsyncAuthenticatedJsonWebsocketConsumer

from .models import Notification


class NotificationConsumer(AsyncAuthenticatedJsonWebsocketConsumer):
    async def connect(self):
        await super().connect()
        if "user" in self.scope:
            channel_layer_name = f"notification-{self.scope['user'].id}"
            await self.channel_layer.group_add(channel_layer_name, self.channel_name)
            # await self.channel_layer.group_send(
            #     channel_layer_name,
            #     {"type": "notification.info", "user_id": self.scope["user"].id},
            # )

    async def get_notification_message(self, user):
        num_unreceived, num_unread = await database_sync_to_async(
            self.get_notification_information
        )(user)
        return f"You have {num_unreceived} new notifications and {num_unread} unread notifications."

    def get_notification_information(self, user):
        qs = Notification.objects.filter(recipient=user)
        num_unreceived = qs.filter(timestamp_received__isnull=True).update(
            timestamp_received=timezone.now()
        )
        num_unread = qs.filter(timestamp_read__isnull=True).count()

        return num_unreceived, num_unread

    async def notification_info(self, content):
        notification_message = await self.get_notification_message(
            get_user_model().objects.get(id=content["user_id"])
        )
        await self.send_json({"title": "Notification", "message": notification_message})

    async def notification_notify(self, content):
        await self.send_json(
            Notification.objects.get(id=content["notification_id"]).to_payload()
        )

    async def receive_json(self, content):
        """ Receives a dict in format of: {"notification_id": <int>} and marks it as received
        """
        database_sync_to_async(
            Notification.objects.filter(id=content["notification_id"]).update(
                timestamp_received=timezone.now()
            )
        )

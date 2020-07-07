from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.utils import timezone

from bridger.websockets.consumers import AsyncAuthenticatedJsonWebsocketConsumer

from .models import Notification


@database_sync_to_async
def get_notification(notification_id):
    return Notification.objects.get(id=notification_id)


@database_sync_to_async
def update_notification(notification_id):
    Notification.objects.filter(id=notification_id).update(timestamp_received=timezone.now())


class NotificationConsumer(AsyncAuthenticatedJsonWebsocketConsumer):
    async def connect(self):
        await super().connect()
        if "user" in self.scope:
            channel_layer_name = f"notification-{self.scope['user'].id}"
            await self.channel_layer.group_add(channel_layer_name, self.channel_name)

    async def get_notification_message(self, user):
        num_unreceived, num_unread = await database_sync_to_async(self.get_notification_information)(user)
        return f"You have {num_unreceived} new notifications and {num_unread} unread notifications."

    def get_notification_information(self, user):
        qs = Notification.objects.filter(recipient=user)
        num_unreceived = qs.filter(timestamp_received__isnull=True).update(timestamp_received=timezone.now())
        num_unread = qs.filter(timestamp_read__isnull=True).count()

        return num_unreceived, num_unread

    async def notification_info(self, content):
        notification_message = await self.get_notification_message(get_user_model().objects.get(id=content["user_id"]))
        await self.send_json({"title": "Notification", "message": notification_message})

    async def notification_notify(self, content):
        notification = await get_notification(notification_id=content["notification_id"])
        await self.send_json(notification.to_payload())

    async def receive_json(self, content):
        """ Receives a dict in format of: {"notification_id": <int>} and marks it as received
        """
        await update_notification(notification_id=content["notification_id"])

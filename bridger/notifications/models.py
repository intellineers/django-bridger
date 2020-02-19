from enum import Enum

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from bridger.buttons import CustomButton, WidgetButton

from .tasks import send_mail, send_system


class NotificationSendType(Enum):
    SYSTEM = "system"
    MAIL = "mail"
    SYSTEM_AND_MAIL = "system_and_mail"


class Notification(models.Model):
    recipient = models.ForeignKey(
        to=get_user_model(), related_name="notifications", on_delete=models.CASCADE
    )

    title = models.CharField(max_length=512)
    message = models.TextField(null=True, blank=True)
    buttons = JSONField(default=list, null=True, blank=True)

    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_received = models.DateTimeField(null=True, blank=True)
    timestamp_read = models.DateTimeField(null=True, blank=True)
    timestamp_mailed = models.DateTimeField(null=True, blank=True)

    send_type_choices = (
        (NotificationSendType.SYSTEM.value, "System"),
        (NotificationSendType.MAIL.value, "Mail"),
        (NotificationSendType.SYSTEM_AND_MAIL.value, "System and Mail"),
    )

    send_type = models.CharField(
        max_length=32,
        choices=send_type_choices,
        default=NotificationSendType.SYSTEM.value,
    )

    def __str__(self):
        return f"{self.recipient} {self.title}"

    def to_payload(self):
        return {
            "id": self.id,
            "title": self.title,
            "message": self.message,
            "buttons": self.buttons,
        }


@receiver(post_save, sender=Notification)
def post_create_notification(sender, instance, created, **kwargs):
    # if created:
    dispatch = {
        NotificationSendType.MAIL.value: [send_mail],
        NotificationSendType.SYSTEM.value: [send_system],
        NotificationSendType.SYSTEM_AND_MAIL.value: [send_system, send_mail],
    }
    for action in dispatch[instance.send_type]:
        action(instance)
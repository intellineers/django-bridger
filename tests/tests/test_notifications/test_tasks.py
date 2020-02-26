import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.db.models.signals import post_save

from bridger.notifications.models import (
    Notification,
    NotificationSendType,
    post_create_notification
)
from bridger.notifications.tasks import send_mail, send_system


@pytest.mark.django_db
class TestNotificationTasks:
    def setup_method(self):
        post_save.disconnect(receiver=post_create_notification, sender=Notification)

        self.user = get_user_model().objects.create(
            username="test_user",
            password="ABC",
            email="test@test.de",
            is_active=True,
            is_superuser=True,
        )
        self.notification = Notification.objects.create(
            recipient=self.user,
            title="New Notification",
            message="You have a new notification",
            send_type=NotificationSendType.MAIL.value,
        )

    def teardown_method(self):
        post_save.connect(receiver=post_create_notification, sender=Notification)

    def test_send_mail(self):
        send_mail(self.notification.id)
        self.notification.refresh_from_db()
        assert len(mail.outbox) == 1
        assert self.notification.timestamp_mailed is not None

    def test_send_system(self):
        # TODO: Mock the async call and check if the correct method was called?
        send_system(self.notification.id)

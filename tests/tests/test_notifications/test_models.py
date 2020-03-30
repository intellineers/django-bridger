from unittest.mock import MagicMock, patch

import celery
import django
import pytest
from django.contrib.auth import get_user_model
from django.test import override_settings

from bridger.notifications.models import Notification, NotificationSendType


@pytest.mark.django_db
class TestNotification:
    def setup_method(self):
        self.user = get_user_model().objects.create(
            username="test_user", password="ABC", is_active=True, is_superuser=True
        )

    def test_str(self, mocker):
        mocker.patch("celery.execute.send_task")

        notification = Notification.objects.create(
            recipient=self.user,
            title="New Notification",
            message="You have a new notification",
        )
        assert str(notification) == f"{notification.recipient} {notification.title}"

    def test_to_payload(self, mocker):
        mocker.patch("celery.execute.send_task")

        notification = Notification.objects.create(
            recipient=self.user,
            title="New Notification",
            message="You have a new notification",
        )
        assert notification.to_payload() == {
            "id": notification.id,
            "title": notification.title,
            "message": notification.message,
            "buttons": notification.buttons,
            "endpoint": None
        }

from unittest.mock import MagicMock, patch

import celery
import pytest
from django.contrib.auth import get_user_model
from django.test import override_settings

import bridger
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
        }

    @pytest.mark.parametrize(
        "send_type, param",
        [
            (NotificationSendType.MAIL.value, "bridger.notifications.send_mail"),
            (NotificationSendType.SYSTEM.value, "bridger.notifications.send_system"),
            (
                NotificationSendType.SYSTEM_AND_MAIL.value,
                [
                    "bridger.notifications.send_mail",
                    "bridger.notifications.send_system",
                ],
            ),
        ],
    )
    def test_post_signal(self, mocker, send_type, param):
        mocker.patch("celery.execute.send_task")

        notification = Notification.objects.create(
            recipient=self.user,
            title="New Notification",
            message="You have a new notification",
            send_type=send_type,
        )

        if isinstance(param, list):
            calls = [
                mocker.call(param[0], args=[notification.id]),
                mocker.call(param[1], args=[notification.id]),
            ]
            assert celery.execute.send_task.call_count == 2
            celery.execute.send_task.assert_has_calls(calls, any_order=True)
        else:
            celery.execute.send_task.assert_called_once_with(
                param, args=[notification.id]
            )

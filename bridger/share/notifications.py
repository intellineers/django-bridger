from bridger.notifications.models import Notification
from bridger.buttons import WidgetButton


def share_notification(user_id, widget_endpoint, message, user):
    _, endpoint = widget_endpoint.split("?widget_endpoint=")
    Notification.objects.create(
        recipient_id=user_id,
        title=f"{user.first_name} {user.last_name} shared a widget with you",
        message=message,
        buttons=[
            dict(WidgetButton(label="Open", icon="wb-icon-data", endpoint=endpoint))
        ],
    )

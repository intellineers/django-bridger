from typing import Dict

from django.conf import settings
from rest_framework.request import Request
from rest_framework.reverse import reverse


def get_notification_config(request: Request) -> Dict:
    scheme = "wss" if request.scheme == "https" else "ws"
    host = request.get_host()
    default_websocket_url = f"{scheme}://{host}/notification/"
    websocket_url = getattr(settings, "BRIDGER_WEBSOCKET_URL", default_websocket_url)

    return {
        "websocket": websocket_url,
        "http": reverse("bridger:notification-list", request=request),
    }

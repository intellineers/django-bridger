from typing import Dict, Tuple

from django.conf import settings
from rest_framework.request import Request
from rest_framework.reverse import reverse


def notification_config(request: Request):
    scheme = "wss" if request.scheme == "https" else "ws"
    host = request.get_host()
    default_websocket_url = f"{scheme}://{host}/ws/notification/"
    websocket_url = getattr(settings, "BRIDGER_WEBSOCKET_URL", default_websocket_url)

    return {
        "websocket": websocket_url,
        "http": reverse("bridger:notification-list", request=request),
    }

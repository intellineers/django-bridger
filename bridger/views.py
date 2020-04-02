import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .enums import AuthType
from .menus import default_registry
from .settings import bridger_settings

logger = logging.getLogger(__name__)


class Menu(APIView):
    @property
    def permission_classes(self):
        bridger_auth = bridger_settings.DEFAULT_AUTH_CONFIG(None)

        if bridger_auth["type"] is None:
            return []

        return [IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(default_registry.to_dict(request))


class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(
            {
                "config": reverse(
                    "bridger:frontenduserconfiguration-list", request=request
                ),
                "name": f"{request.user.first_name} {request.user.last_name}",
                "email": request.user.email,
                "image": "TODO: Here comes the URL",
            }
        )


class Config(APIView):
    permission_classes = []

    def get(self, request: Request) -> Response:
        return Response(
            {
                "authentication": bridger_settings.DEFAULT_AUTH_CONFIG(request),
                "profile": reverse("bridger:profile", request=request),
                "menu": reverse("bridger:menu", request=request),
                "notification": bridger_settings.DEFAULT_NOTIFICATION_CONFIG(
                    request=request
                ),
            }
        )

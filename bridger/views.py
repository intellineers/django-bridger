import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .buttons import ActionButton
from .display import FieldSet, InstanceDisplay, Section
from .enums import AuthType
from .menus import default_registry
from .settings import bridger_settings
from .share import ShareSerializer

logger = logging.getLogger(__name__)


class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(
            {
                "config": reverse("bridger:frontenduserconfiguration-list", request=request),
                "name": f"{request.user.first_name} {request.user.last_name}",
                "email": request.user.email,
                "profile": bridger_settings.PROFILE(request),
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
                "notification": bridger_settings.DEFAULT_NOTIFICATION_CONFIG(request=request),
                "share": dict(bridger_settings.DEFAULT_SHARE_BUTTON(request=request)),
                "markdown": {"blockdiag": reverse("bridger:blockdiag", request=request)},
                "clubhouse": bridger_settings.CLUBHOUSE_CONFIG(request),
            }
        )

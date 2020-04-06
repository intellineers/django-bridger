import logging

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .buttons import ActionButton
from .display import InstanceDisplay, Section, FieldSet
from .enums import AuthType
from .menus import default_registry
from .settings import bridger_settings

from .share import ShareSerializer

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


class Share(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        user_id = request.POST.get("user_id", None)
        widget_endpoint = request.POST.get("widget_endpoint", None)

        return Response({})


class Config(APIView):
    permission_classes = []

    def get(self, request: Request) -> Response:
        btn = ActionButton(
            label="Share",
            icon="wb-icon-trade",
            endpoint=reverse("bridger:share", request=request),
            instance_display=InstanceDisplay(
                sections=[
                    Section(fields=FieldSet(fields=["user_id", "widget_endpoint"]))
                ]
            ),
            serializer=ShareSerializer,
        )
        btn.request = request

        return Response(
            {
                "authentication": bridger_settings.DEFAULT_AUTH_CONFIG(request),
                "profile": reverse("bridger:profile", request=request),
                "menu": reverse("bridger:menu", request=request),
                "notification": bridger_settings.DEFAULT_NOTIFICATION_CONFIG(
                    request=request
                ),
                "share": dict(btn),
            }
        )

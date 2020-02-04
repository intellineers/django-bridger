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
from .settings import get_bridger_auth

logger = logging.getLogger(__name__)


class Menu(APIView):
    @property
    def permission_classes(self):
        bridger_auth = get_bridger_auth(None)

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
                "image": "TODO: Here comes the URL",
            }
        )


class Config(APIView):
    permission_classes = []

    def get(self, request: Request) -> Response:
        # TODO: This needs to be a bit more flexible if the user wants to change something
        return Response(
            {
                "authentication": get_bridger_auth(request),
                "profile": reverse("bridger:profile", request=request),
                "menu": reverse("bridger:menu", request=request),
                "notification": {},
            }
        )

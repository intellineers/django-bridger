from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .enums import AuthType
from .menus import default_registry


class Menu(APIView):
    # permission_classes = [IsAuthenticated]

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
    def get(self, request: Request) -> Response:
        auth = getattr(settings, "BRIDGER_AUTH")

        return Response(
            {
                # "authentication": auth(request),
                "authentication": {"type": AuthType.NONE.name},
                "notification": {},
                "profile": reverse("bridger:profile", request=request),
                # "profile": {},
                "menu": reverse("bridger:menu", request=request),
            }
        )

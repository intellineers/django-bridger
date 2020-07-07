from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from bridger.settings import bridger_settings

from .registry import default_registry


class MenuAPIView(APIView):
    @property
    def permission_classes(self):
        bridger_auth = bridger_settings.DEFAULT_AUTH_CONFIG(None)

        if bridger_auth["type"] is None:
            return []

        return [IsAuthenticated]

    def get(self, request: Request) -> Response:
        default_registry.request = request
        return Response(list(default_registry))

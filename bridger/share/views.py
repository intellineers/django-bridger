from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from bridger.settings import bridger_settings


class ShareAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = bridger_settings.DEFAULT_SHARE_SERIALIZER(data=request.data)
        serializer.is_valid(raise_exception=True)
        bridger_settings.DEFAULT_SHARE_NOTIFICATION(**request.data, user=request.user)
        return Response({})

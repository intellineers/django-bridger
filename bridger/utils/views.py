from django.conf import settings
from django.urls.exceptions import NoReverseMatch
from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.pagination import CursorPagination
from django_filters.rest_framework import DjangoFilterBackend

def get_full_widget_url(reverse_path):
    return  f'{settings.BASE_ENDPOINT_URL}?widget_endpoint={settings.BASE_ENDPOINT_URL}{reverse_path}'

def set_identifier(identifier):
    def decorator(func):
        func.identifier = identifier
        return func

    return decorator

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_endpoints_root(request, format=None):
    try:
        endpoints = dict()
        for wb_endpoint in settings.WB_ENDPOINTS:
            try:
                endpoints[wb_endpoint] = reverse(
                    f"{wb_endpoint}:api-root", request=request, format=format
                )
            except NoReverseMatch:
                pass

        return Response(endpoints)

    except AttributeError:
        return Response(
            {"error": "No Endpoints specified."}, status=status.HTTP_400_BAD_REQUEST
        )

import logging

import django_filters
from django.db.models import QuerySet
from django.urls.exceptions import NoReverseMatch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .fsm.mixins import FSMViewSetMixin
from .filters import BooleanFilter, ModelChoiceFilter
from .mixins import MetadataMixin
from .pagination import CursorPagination

logger = logging.getLogger(__name__)


class RepresentationModelViewSet(MetadataMixin, viewsets.ReadOnlyModelViewSet):
    """A Representation View that is used for serializing related fields"""

    filter_backends = [filters.OrderingFilter]
    pagination_class = CursorPagination

    ordering_fields = ordering = ["id"]


class ModelViewSet(MetadataMixin, FSMViewSetMixin, viewsets.ModelViewSet):
    """A Model View that is used to serializer models"""

    filter_backends = [filters.OrderingFilter]
    pagination_class = CursorPagination

    ordering_fields = ordering = ["id"]

    @classmethod
    def get_model(cls):
        try:
            if hasattr(cls, "queryset"):
                return cls.queryset.model
            elif hasattr(cls, "serializer_class"):
                return cls.serializer_class.Meta.model
            else:
                return None
        except AttributeError:
            return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serialized_content = {"instance": serializer.data}

        if hasattr(self, "get_messages"):
            serialized_content["messages"] = self.get_messages(request)

        return Response(serialized_content)


class ChartViewSet(MetadataMixin, ListModelMixin, viewsets.ViewSet):
    """A List View that is used for creating plotly charts"""

    CHART_DISPLAY = True
    filter_backends = [DjangoFilterBackend]

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_endpoints_root(request: Request, format: str = None) -> Response:
    """Returns a list of API-ROOT endpoints specified in BRIDGER_ENDPOINTS"""

    endpoints = dict()
    endpoints["config"] = reverse("bridger:config", request=request, format=format)

    if hasattr(settings, "BRIDGER_ENDPOINTS"):
        for bridger_endpoint in settings.BRIDGER_ENDPOINTS:
            try:
                endpoints[bridger_endpoint] = reverse(
                    f"{bridger_endpoint}:api-root", request=request, format=format
                )
            except NoReverseMatch:
                endpoints[bridger_endpoint] = reverse(
                    f"API-ROOT of {bridger_endpoint} is not yet implemented."
                )

    return Response(endpoints, status=status.HTTP_200_OK)

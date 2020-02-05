import logging

import django_filters
from django.conf import settings
from django.db.models import QuerySet
from django.urls.exceptions import NoReverseMatch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .enums import WidgetType
from .filters import BooleanFilter, ModelChoiceFilter
from .fsm.mixins import FSMViewSetMixin
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

    def destroy_multiple(self, request, *args, **kwargs):
        model = self.get_serializer_class().Meta.model
        app_label = model._meta.app_label

        queryset = model.objects.filter(id__in=request.data)
        destroyed = self.perform_destroy_multiple(queryset)

        return Response(
            {"count": destroyed[1].get(f"{app_label}.{model.__name__}", 0)},
            status=status.HTTP_204_NO_CONTENT,
        )

    def perform_destroy_multiple(self, queryset):
        return queryset.delete()


class InfiniteDataModelView(ModelViewSet):

    pagination_class = None

    def list(self, request, *args, **kwargs) -> Response:
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        aggregates = dict()
        messages = dict()
        if hasattr(self, "get_aggregates"):
            aggregates = self.get_aggregates(queryset, queryset)

        if hasattr(self, "get_messages"):
            messages = self.get_messages(self.request, queryset, queryset)

        return Response(
            {"results": serializer.data, "aggregates": aggregates, "messages": messages}
        )


class ChartViewSet(MetadataMixin, ListModelMixin, viewsets.ViewSet):
    """A List View that is used for creating plotly charts"""

    WIDGET_TYPE = WidgetType.CHART.value
    filter_backends = [DjangoFilterBackend]

    def list(self, request, *args, **kwargs):
        figure = self.get_plotly(self.filter_queryset(self.get_queryset()))
        figure_dict = figure.to_plotly_json()
        figure_dict["config"] = {"responsive": True, "displaylogo": False}
        figure_dict["useResizeHandler"] = True
        figure_dict["style"] = {"width": "100%", "height": "100%"}

        return Response(figure_dict)

    def get_queryset(self):
        return self.queryset

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

from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ViewSetMixin

from bridger.enums import Button, WidgetType
from bridger.fsm.mixins import FSMViewSetMixin
from bridger.metadata.views import MetadataMixin
from bridger.pagination import CursorPagination

from .generics import GenericAPIView
from .mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    DestroyMultipleModelMixin,
    FilterMixin,
    ListModelMixin,
    ModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)


class GenericViewSet(ViewSetMixin, GenericAPIView):
    pass


class ViewSet(MetadataMixin, ViewSet):
    def get_serializer(self):
        return self.serializer_class()

    def get_serializer_class(self):
        return getattr(self, "serializer_class", None)


class ReadOnlyModelViewSet(
    MetadataMixin,
    ModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    FilterMixin,
    GenericViewSet,
):
    pagination_class = CursorPagination
    READ_ONLY = True
    CREATE_BUTTONS = []
    BUTTONS = [Button.REFRESH.value]


class ModelViewSet(
    FSMViewSetMixin,
    MetadataMixin,
    ModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    DestroyMultipleModelMixin,
    ListModelMixin,
    FilterMixin,
    GenericViewSet,
):
    pagination_class = CursorPagination


class ReadOnlyInfiniteModelViewSet(ReadOnlyModelViewSet):
    pagination_class = None


RepresentationModelViewSet = ReadOnlyModelViewSet


class InfiniteDataModelView(ModelViewSet):
    pagination_class = None


class ChartViewSet(FilterMixin, ViewSet):

    WIDGET_TYPE = WidgetType.CHART.value

    def list(self, request: Request, *args, **kwargs):
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

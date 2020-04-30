from rest_framework.viewsets import ViewSetMixin, ViewSet

from bridger.enums import WidgetType
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
        return self.serializer_class


class ReadOnlyModelViewSet(
    MetadataMixin,
    ModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    FilterMixin,
    GenericViewSet,
):
    pagination_class = CursorPagination


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

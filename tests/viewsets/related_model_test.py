from typing import Optional

from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.request import Request

from bridger import buttons as bt
from bridger import display as dp
from bridger.auth import JWTCookieAuthentication
from bridger.enums import Unit
from bridger.messages import info
from bridger.pagination import LimitOffsetPagination
from bridger.serializers import ListSerializer
from bridger.viewsets import ModelViewSet, ReadOnlyModelViewSet, RepresentationViewSet
from tests.models import ModelTest, RelatedModelTest
from tests.serializers import ActionButtonSerializer, RelatedModelTestRepresentationSerializer, RelatedModelTestSerializer

from .buttons import RelatedModelTestButtonConfig
from .display import RelatedModelTestDisplayConfig





class RelatedModelTestRepresentationViewSet(RepresentationViewSet):
    queryset = RelatedModelTest.objects.all()
    serializer_class = RelatedModelTestRepresentationSerializer


class RelatedModelTestModelViewSet(ModelViewSet):
    pagination_class = LimitOffsetPagination

    ENDPOINT = "relatedmodeltest-list"

    display_config_class = RelatedModelTestDisplayConfig
    button_config_class = RelatedModelTestButtonConfig

    filter_fields = {"model_test": ["exact"], "char_field": ["exact"]}
    search_fields = ["char_field"]
    ordering_fields = ["id", "model_test__char_field"]
    queryset = RelatedModelTest.objects.all()
    serializer_class = RelatedModelTestSerializer

    def get_messages(self, instance=None, initial=None, **kwargs):
        if instance:
            return [info("This is an instance message.")]
        if initial:
            return [info("This is a list message")]

    def get_serializer_changes(self, serializer):
        if not isinstance(serializer, ListSerializer) and hasattr(serializer, "fields"):
            if "model_tests" in serializer.fields:
                default_values = ModelTest.objects.all()[:3].values_list("id", flat=True)
                serializer.fields["model_tests"].child_relation.default = default_values
        return serializer

    @action(
        detail=True,
        methods=["GET"],
        authentication_classes=[JWTCookieAuthentication],
        permission_classes=[],
        renderer_classes=[StaticHTMLRenderer],
    )
    def authenticated_html(self, request, pk):
        return HttpResponse(f"<h1>Hello World {request.user}</h1>")

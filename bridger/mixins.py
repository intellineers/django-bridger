import logging
from collections import defaultdict
from typing import Dict, Generator, Iterator, List, Optional, Tuple, Union

from django.contrib.contenttypes.models import ContentType
from rest_framework import filters
from rest_framework.pagination import CursorPagination, LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.reverse import reverse

from bridger.enums import Button, WidgetType
from bridger.filters import DjangoFilterBackend
from bridger.serializers import ListSerializer, RepresentationSerializer

from .metadata import BridgerMetaData
from .utils import ilen

logger = logging.getLogger(__name__)

# FIELD         --> Default Value
# get_field     --> Default Implementation
# _get_field    --> Transformation


class MetadataMixin(
    IdentifierMetadataMixin, WidgetTypeMetadataMixin, EndpointMetadataMixin
):
    metadata_class = BridgerMetaData

    def get_instance_display(self, request: Request) -> List:
        if hasattr(self, "INSTANCE_DISPLAY"):
            return self.INSTANCE_DISPLAY.to_dict()
        return []

    def get_list_display(self, request: Request) -> Dict:
        if hasattr(self, "LIST_DISPLAY"):
            return self.LIST_DISPLAY.to_dict()
        return {}

    def get_fields(self, request: Request) -> Dict:
        fields = dict()
        rs = RepresentationSerializer
        ls = ListSerializer
        field_items = self.get_serializer().fields.items()

        for name, field in filter(
            lambda f: not isinstance(f[1], (rs, ls)), field_items
        ):
            fields[name] = field.get_representation(request, name)

        for name, field in filter(lambda f: isinstance(f[1], (rs, ls)), field_items):
            representation = field.get_representation(request, name)
            fields[representation["related_key"]].update(representation)
            del fields[representation["related_key"]]["related_key"]

        return fields

    def get_preview_display(self, request: Request):
        return getattr(self, "PREVIEW_DISPLAY", "")

    def get_preview_buttons(self, request: Request):
        return [button.to_dict() for button in getattr(self, "PREVIEW_BUTTONS", [])]

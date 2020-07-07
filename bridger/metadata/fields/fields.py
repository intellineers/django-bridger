from typing import Dict, Union

from rest_framework.request import Request

from bridger.metadata.mixins import BridgerMetadataMixin
from bridger.serializers import ListSerializer, RepresentationSerializer, percent_decorator


class FieldsMetadata(BridgerMetadataMixin):
    key = "fields"
    method_name = "_get_fields"


class FieldsMetadataMixin:
    def get_fields(self, request: Request) -> Dict:
        fields = dict()
        rs = RepresentationSerializer
        ls = ListSerializer
        field_items = self.get_serializer().fields.items()

        for name, field in filter(lambda f: not isinstance(f[1], (rs, ls)), field_items):
            fields[name] = field.get_representation(request, name)

        for name, field in filter(lambda f: isinstance(f[1], (rs, ls)), field_items):
            representation = field.get_representation(request, name)
            fields[representation["related_key"]].update(representation)
            del fields[representation["related_key"]]["related_key"]

        return fields

    def _get_fields(self, request: Request) -> Dict:
        fields = self.get_fields(request)
        serializer_class = self.get_serializer_class()

        for key, value in serializer_class.get_decorators():
            fields[key]["decorators"].append(value)
        for key in serializer_class.get_percent_fields():
            fields[key]["type"] = "percent"
            fields[key]["decorators"].append(percent_decorator)

        return fields

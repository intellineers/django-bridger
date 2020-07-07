from rest_framework import filters
from rest_framework.request import Request

from bridger.filters import DjangoFilterBackend
from bridger.metadata.mixins import BridgerMetadataMixin
from bridger.utils import ilen


class FilterFieldsMetadata(BridgerMetadataMixin):
    key = "filter_fields"
    method_name = "_get_filter_fields"


class FilterFieldsMetadataMixin:
    def get_filter_fields(self, request: Request):
        if DjangoFilterBackend in getattr(self, "filter_backends", []):
            filterset_class = DjangoFilterBackend().get_filterset_class(self, self.queryset)
            if hasattr(filterset_class, "base_filters"):
                filterset = filterset_class.base_filters.items()
                field_names = [v.field_name for k, v in filterset_class.base_filters.items()]
                stored_fields = dict()
                for index, (name, field) in enumerate(filterset):

                    upcomming_fields = ilen(filter(lambda f: f == field.field_name, field_names[index + 1 :]))
                    representation = field.get_representation(request, name, self)

                    if upcomming_fields > 0 or field.field_name in stored_fields:
                        _representation = stored_fields.get(field.field_name, representation)
                        _representation["lookup_expr"].update(representation["lookup_expr"])
                        _representation["default"].update(representation["default"])
                        stored_fields[field.field_name] = _representation

                    if upcomming_fields == 0:
                        yield field.field_name, stored_fields.get(field.field_name, representation)

    def _get_filter_fields(self, request: Request):
        return dict(self.get_filter_fields(request))

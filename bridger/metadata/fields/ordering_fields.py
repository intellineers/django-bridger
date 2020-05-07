from rest_framework import filters
from rest_framework.request import Request

from bridger.metadata.mixins import BridgerMetadataMixin


class OrderingFieldsMetadata(BridgerMetadataMixin):
    key = "ordering_fields"
    method_name = "_get_ordering_fields"


class OrderingFieldsMetadataMixin:
    def get_ordering_fields(self, request: Request):
        if filters.OrderingFilter in getattr(self, "filter_backends", []):
            for ordering_field in self.ordering_fields:
                if "__" in ordering_field:
                    yield ordering_field.split("__")[0], ordering_field
                else:
                    yield ordering_field, ordering_field

    def _get_ordering_fields(self, request: Request):
        return dict(self.get_ordering_fields(request=request))

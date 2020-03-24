from rest_framework.request import Request
from rest_framework import filters
from bridger.metadata.mixins import BridgerMetadataMixin


class OrderingFieldsMetadata(BridgerMetadataMixin):
    key = "ordering_fields"
    method_name = "_get_ordering_fields"


class OrderingFieldsMetadataMixin:
    def _get_ordering_fields(self, request: Request):
        if filters.OrderingFilter in self.filter_backends:
            yield from self.ordering_fields

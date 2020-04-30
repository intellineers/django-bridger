from rest_framework import filters
from rest_framework.request import Request

from bridger.metadata.mixins import BridgerMetadataMixin


class SearchFieldsMetadata(BridgerMetadataMixin):
    key = "search_fields"
    method_name = "_get_search_fields"


class SearchFieldsMetadataMixin:
    def _get_search_fields(self, request: Request):
        if filters.SearchFilter in getattr(self, "filter_backends", []):
            yield from self.search_fields

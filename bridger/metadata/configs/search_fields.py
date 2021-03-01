from typing import Dict

from bridger.metadata.mixins import BridgerViewSetConfig
from bridger.filters import DjangoFilterBackend
from bridger.utils import ilen

from rest_framework.filters import SearchFilter
from rest_fuzzysearch.search import RankedFuzzySearchFilter

class SearchFieldsBridgerViewSetConfig(BridgerViewSetConfig):

    def get_metadata(self) -> str:
        if SearchFilter in getattr(self.view, "filter_backends", []) or RankedFuzzySearchFilter in getattr(self.view, "filter_backends", []):
            return self.view.search_fields

    @classmethod
    def get_metadata_key(cls):
        return "search_fields"

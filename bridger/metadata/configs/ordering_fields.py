from typing import Dict

from bridger.metadata.mixins import BridgerViewSetConfig
from bridger.filters import DjangoFilterBackend
from bridger.utils import ilen

from rest_framework.filters import OrderingFilter

class OrderingFieldsBridgerViewSetConfig(BridgerViewSetConfig):

    def get_metadata(self) -> str:
        if OrderingFilter in getattr(self.view, "filter_backends", []):
            for ordering_field in self.view.ordering_fields:
                if "__" in ordering_field:
                    yield ordering_field.split("__")[0], ordering_field
                else:
                    yield ordering_field, ordering_field

    @classmethod
    def get_metadata_key(cls):
        return "ordering_fields"

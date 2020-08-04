from typing import Dict

from bridger.metadata.mixins import BridgerViewSetConfig


class PaginationBridgerViewSetConfig(BridgerViewSetConfig):

    def get_metadata(self) -> str:
        pagination = self.view.pagination_class.__name__ if self.view.pagination_class else None
        return {
            "CursorPagination": "cursor",
            "LimitOffsetPagination": "limitoffset",
            None: None
        }[pagination] 

    @classmethod
    def get_metadata_key(cls):
        return "pagination"

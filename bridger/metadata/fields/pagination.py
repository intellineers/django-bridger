from rest_framework.request import Request

from bridger.metadata.mixins import BridgerMetadataMixin


class PaginationMetadata(BridgerMetadataMixin):
    key = "pagination"
    method_name = "_get_pagination"


class PaginationMetadataMixin:
    def _get_pagination(self, request: Request):
        pagination = self.pagination_class.__name__ if hasattr(self, "pagination_class") and self.pagination_class else None

        return {"CursorPagination": "cursor", "LimitOffsetPagination": "limitoffset", None: None,}[pagination]

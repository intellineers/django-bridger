from typing import Dict, Union

from rest_framework.request import Request

from bridger.display import Calendar, InstanceDisplay, ListDisplay
from bridger.metadata.mixins import BridgerMetadataMixin


class PKMetadata(BridgerMetadataMixin):
    key = "pk"
    method_name = "_get_pk"


class PKMetadataMixin:
    def get_pk(self, request: Request, pk=None):
        if pk:
            return pk

        return self.kwargs.get("pk", None)

    def _get_pk(self, request: Request):
        return self.get_pk(request=request, pk=getattr(self, "PK", None))

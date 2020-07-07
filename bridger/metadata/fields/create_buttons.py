from typing import List

from rest_framework.request import Request

from bridger.enums import Button
from bridger.metadata.mixins import BridgerMetadataMixin


class CreateButtonMetadata(BridgerMetadataMixin):
    key = "create_buttons"
    method_name = "_get_create_buttons"


class CreateButtonMetadataMixin:
    def get_create_buttons(self, request: Request, buttons: List[str] = None) -> List[str]:
        return buttons or Button.create_buttons()

    def _get_create_buttons(self, request: Request) -> List[str]:
        return self.get_create_buttons(request=request, buttons=getattr(self, "CREATE_BUTTONS", None))

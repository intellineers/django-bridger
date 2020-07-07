from typing import List

from rest_framework.request import Request

from bridger.buttons.bases import ButtonConfig as Button
from bridger.metadata.mixins import BridgerMetadataMixin


class CustomButtonMetadata(BridgerMetadataMixin):
    key = "custom_buttons"
    method_name = "_get_custom_buttons"


class CustomButtonMetadataMixin:
    def get_custom_buttons(self, request: Request, buttons: List) -> List:
        return buttons

    def _get_custom_buttons(self, request: Request) -> List:
        buttons = self.get_custom_buttons(request=request, buttons=getattr(self, "CUSTOM_BUTTONS", []))
        button_list = list()
        for button in buttons:
            button.request = request
            button_list.append(dict(button))
        return button_list

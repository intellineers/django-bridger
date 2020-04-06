from typing import List

from rest_framework.request import Request

from bridger.buttons.bases import ButtonConfig as Button
from bridger.metadata.mixins import BridgerMetadataMixin


class CustomInstanceButtonMetadata(BridgerMetadataMixin):
    key = "custom_instance_buttons"
    method_name = "_get_custom_instance_buttons"


class CustomInstanceButtonMetadataMixin:
    def get_custom_list_instance_buttons(self, request: Request, buttons: List) -> List:
        return buttons

    def get_custom_instance_buttons(self, request: Request, buttons: List) -> List:
        return buttons

    def _get_custom_instance_buttons(self, request: Request) -> List:
        if "pk" in self.kwargs:
            buttons = self.get_custom_instance_buttons(
                request=request, buttons=getattr(self, "CUSTOM_INSTANCE_BUTTONS", [])
            )
            button_list = list()
            for button in buttons:
                button.request = request
                button_list.append(dict(button))
            return button_list
        else:
            buttons = self.get_custom_list_instance_buttons(
                request=request,
                buttons=getattr(self, "CUSTOM_LIST_INSTANCE_BUTTONS", []),
            )
            button_list = list()
            for button in buttons:
                button.request = request
                button_list.append(dict(button))
            return button_list

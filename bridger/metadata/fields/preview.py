from typing import Dict, Union

from rest_framework.request import Request

from bridger.metadata.mixins import BridgerMetadataMixin


class PreviewMetadata(BridgerMetadataMixin):
    key = "preview"
    method_name = "_get_preview"


class PreviewMetadataMixin:
    def get_preview_buttons(self, request: Request, buttons):
        return buttons

    def get_preview_display(self, request: Request, display):
        return display

    def get_preview_type(self, request: Request, preview_type):
        return preview_type

    def _get_preview_display(self, request: Request, display, preview_type):
        if preview_type == "html":
            return display
        elif preview_type == "instance_display":
            return list(display)

    def _get_preview(self, request: Request) -> Dict:
        buttons = self.get_preview_buttons(request=request, buttons=getattr(self, "PREVIEW_BUTTONS", []))
        button_list = list()

        for button in buttons:
            button_list.append(dict(button))

        preview_type = self.get_preview_type(request, getattr(self, "PREVIEW_TYPE", "html"))

        _display = self.get_preview_display(request, getattr(self, "PREVIEW_DISPLAY", None))
        display = self._get_preview_display(request=request, display=_display, preview_type=preview_type)

        return {"buttons": button_list, "display": display, "type": preview_type}

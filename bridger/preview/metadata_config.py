from typing import Optional

from rest_framework.request import Request
from bridger.metadata.mixins import BridgerViewSetConfig


class PreviewConfig(BridgerViewSetConfig):
    DISPLAY_TYPE = "instance_display"

    def get_buttons(self):
        return []

    def _get_buttons(self):
        return [dict(button) for button in self.get_buttons()]

    def get_display(self):
        return None

    def _get_display(self):
        if display := self.get_display():
            if self.DISPLAY_TYPE == "instance_display":
                return list(display)
            return display
        return None

    def _get_display_type(self):
        return self.DISPLAY_TYPE

    def get_metadata(self):
        buttons = self._get_buttons()
        display = self._get_display()

        if len(buttons) > 0 or display is not None:
            yield "buttons", buttons
            yield "display", display
            yield "type", self._get_display_type()

    @classmethod
    def get_metadata_key(cls):
        return "preview"

    @classmethod
    def get_metadata_fieldname(cls):
        return "preview_config_class"


class PreviewConfigMixin:
    preview_config_class = PreviewConfig

from typing import Optional

from rest_framework.request import Request

from bridger.display.instance_display import InstanceDisplay
from bridger.display.list_display import ListDisplay
from bridger.metadata.mixins import BridgerViewSetConfig


class DisplayConfig(BridgerViewSetConfig):
    def get_instance_display(self) -> Optional[InstanceDisplay]:
        return None

    def get_list_display(self) -> Optional[ListDisplay]:
        return None

    def get_preview_display(self) -> Optional[InstanceDisplay]:
        return None

    def get_metadata(self):
        yield "instance", list(self.get_instance_display() or [])
        yield "preview", list(self.get_preview_display() or [])
        if not self.instance:
            yield "list", dict(self.get_list_display() or {})

    @classmethod
    def get_metadata_key(cls):
        return "display"

    @classmethod
    def get_metadata_fieldname(cls):
        return "display_config_class"


class DisplayConfigMixin:
    display_config_class = DisplayConfig

from typing import Dict

from bridger.metadata.mixins import BridgerViewSetConfig

from bridger.enums import WidgetType

class TypeBridgerViewSetConfig(BridgerViewSetConfig):

    def get_metadata(self) -> str:
        return WidgetType.INSTANCE.value if self.instance else WidgetType.LIST.value

    @classmethod
    def get_metadata_key(cls):
        return "type"

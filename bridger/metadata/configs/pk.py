from typing import Dict

from bridger.metadata.mixins import BridgerViewSetConfig


class PKBridgerViewSetConfig(BridgerViewSetConfig):

    def get_metadata(self) -> Dict:
        return self.view.kwargs.get("pk", None)

    @classmethod
    def get_metadata_key(cls):
        return "pk"

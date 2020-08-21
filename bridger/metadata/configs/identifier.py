from typing import Dict

from bridger.metadata.mixins import BridgerViewSetConfig


class IdentifierBridgerViewSetConfig(BridgerViewSetConfig):

    def get_metadata(self) -> str:
        if identifier := getattr(self.view, "IDENTIFIER", None):
            return identifier

        # assert hasattr(self.view, "get_content_type"), "View(Set) has to define an IDENTIFIER, if no content"
        content_type = self.view.get_content_type()
        return "{0.app_label}:{0.model}".format(content_type)

    @classmethod
    def get_metadata_key(cls):
        return "identifier"

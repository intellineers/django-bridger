from typing import Dict

from rest_framework.reverse import reverse

from bridger.metadata.mixins import BridgerViewSetConfig


class DocumentationBridgerViewSetConfig(BridgerViewSetConfig):
    def get_metadata(self) -> str:
        if self.view._get_documentation_path(self.instance) and self.view.basename:
            if self.instance:
                reverse_name = f"{self.view.basename}-instance-documentation"
                args = [self.view.kwargs.get("pk")]
            else:
                reverse_name = f"{self.view.basename}-list-documentation"
                args = []
            return reverse(reverse_name, args=args, request=self.request)

        return None

    @classmethod
    def get_metadata_key(cls):
        return "documentation"

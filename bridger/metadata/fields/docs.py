from typing import List

from django.contrib.contenttypes.models import ContentType
from rest_framework.request import Request
from rest_framework.reverse import reverse

from bridger.enums import Button
from bridger.metadata.mixins import BridgerMetadataMixin


class DocsMetadata(BridgerMetadataMixin):
    key = "docs"
    method_name = "_get_docs"


class DocsMetadataMixin:
    def _get_docs(self, request: Request) -> str:
        pk = self.kwargs.get("pk", None)
        endpoints = self._get_endpoints(request)

        if hasattr(self, "basename"):
            if self.basename and pk and hasattr(self, "INSTANCE_DOCS"):
                return reverse(viewname=f"{self.basename}-instance-docs", args=[pk], request=request,)

            if self.basename and hasattr(self, "LIST_DOCS"):
                return reverse(viewname=f"{self.basename}-list-docs", request=request)

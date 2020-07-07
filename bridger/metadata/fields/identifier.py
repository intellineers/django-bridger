from django.contrib.contenttypes.models import ContentType
from rest_framework.request import Request

from bridger.metadata.mixins import BridgerMetadataMixin


class IdentifierMetadata(BridgerMetadataMixin):
    key = "identifier"
    method_name = "_get_identifier"


class IdentifierMetadataMixin:
    def get_identifier(self, request: Request, identifier: str = None) -> str:
        assert identifier is not None or hasattr(
            self, "get_serializer_class"
        ), "Viewsets without serializer classes need to set IDENTIFIER or override get_identifier"

        return identifier or "{0.app_label}:{0.model}".format(
            ContentType.objects.get_for_model(self.get_serializer_class().Meta.model)
        )

    def _get_identifier(self, request: Request) -> str:
        return self.get_identifier(request=request, identifier=getattr(self, "IDENTIFIER", None))

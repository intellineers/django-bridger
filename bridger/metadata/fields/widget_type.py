from rest_framework.request import Request

from bridger.enums import WidgetType
from bridger.metadata.mixins import BridgerMetadataMixin


class WidgetTypeMetadata(BridgerMetadataMixin):
    key = "type"
    method_name = "_get_widget_type"


class WidgetTypeMetadataMixin:
    def get_widget_type(self, request: Request, widget_type: str = None) -> str:
        return widget_type or (WidgetType.LIST.value if "pk" not in self.kwargs else WidgetType.INSTANCE.value)

    def _get_widget_type(self, request: Request) -> str:
        return self.get_widget_type(request=request, widget_type=getattr(self, "WIDGET_TYPE", None))

from typing import Dict, Union

from rest_framework.request import Request

from bridger.display import Calendar, InstanceDisplay, ListDisplay
from bridger.metadata.mixins import BridgerMetadataMixin


class InstanceDisplayMetadata(BridgerMetadataMixin):
    key = "instance_display"
    method_name = "_get_instance_display"


class InstanceDisplayMetadataMixin:
    def get_instance_display(self, request: Request, display: InstanceDisplay = None) -> InstanceDisplay:
        return display or []

    def _get_instance_display(self, request: Request) -> Dict:
        return list(self.get_instance_display(request=request, display=getattr(self, "INSTANCE_DISPLAY", None)))


class ListDisplayMetadata(BridgerMetadataMixin):
    key = "list_display"
    method_name = "_get_list_display"


class ListDisplayMetadataMixin:
    def get_list_display(self, request: Request, display: Union[ListDisplay, Calendar] = None) -> Union[ListDisplay, Calendar]:
        return display or {}

    def _get_list_display(self, request: Request) -> Dict:
        return dict(self.get_list_display(request=request, display=getattr(self, "LIST_DISPLAY", None)))

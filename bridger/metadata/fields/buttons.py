from typing import List

from django.contrib.contenttypes.models import ContentType
from rest_framework.request import Request

from bridger.enums import Button
from bridger.metadata.mixins import BridgerMetadataMixin


class ButtonMetadata(BridgerMetadataMixin):
    key = "buttons"
    method_name = "_get_buttons"


class ButtonMetadataMixin:
    def get_instance_buttons(self, request: Request, buttons: List[str] = None) -> List[str]:
        if buttons:
            return buttons

        button_list = list()

        if hasattr(self, "get_serializer_class"):
            serializer_class = self.get_serializer_class()
            if hasattr(serializer_class, "Meta"):
                model = self.get_serializer_class().Meta.model
                ct = ContentType.objects.get_for_model(model)

                if request.user.has_perm(f"{ct.app_label}.change_{ct.model}"):
                    button_list.append(Button.SAVE.value)
                if request.user.has_perm(f"{ct.app_label}.delete_{ct.model}"):
                    button_list.append(Button.DELETE.value)

        return button_list

    def _get_instance_buttons(self, request: Request) -> List[str]:
        return self.get_instance_buttons(request=request, buttons=getattr(self, "INSTANCE_BUTTONS", None))

    def get_list_buttons(self, request: Request, buttons: List[str] = None) -> List[str]:
        if buttons:
            return buttons

        button_list = list()

        if hasattr(self, "get_serializer_class"):
            serializer_class = self.get_serializer_class()
            if hasattr(serializer_class, "Meta"):
                model = self.get_serializer_class().Meta.model
                ct = ContentType.objects.get_for_model(model)

                if f"{ct.app_label}.add_{ct.model}":
                    button_list.append(Button.NEW.value)

        return button_list

    def _get_list_buttons(self, request: Request) -> List[str]:
        return self.get_list_buttons(request=request, buttons=getattr(self, "LIST_BUTTONS", None))

    def get_buttons(self, request: Request, buttons: List[str] = None) -> List[str]:
        if buttons:
            return buttons

        button_list = list()

        pk = self.kwargs.get("pk", None)

        if pk:
            button_list.extend(self._get_instance_buttons(request))
        else:
            button_list.extend(self._get_list_buttons(request))

        button_list.append(Button.REFRESH.value)

        return set(button_list)

    def _get_buttons(self, request: Request) -> str:
        return self.get_buttons(request=request, buttons=getattr(self, "BUTTONS", None))

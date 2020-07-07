from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from rest_framework.request import Request

from bridger.display import InstanceDisplay
from bridger.enums import RequestType
from bridger.serializers import ListSerializer, RepresentationSerializer, Serializer

from .bases import ButtonConfig, ButtonTypeMixin, ButtonUrlMixin
from .enums import ButtonType, HyperlinkTarget


@dataclass
class DropDownButton(ButtonTypeMixin, ButtonConfig):
    button_type = ButtonType.DROPDOWN
    buttons: List = field(default_factory=list)

    def get_buttons(self):
        for button in self.buttons:
            if hasattr(self, "request"):
                button.request = self.request
            yield dict(button)

    def __iter__(self):
        yield from super().__iter__()
        yield "buttons", self.get_buttons()


@dataclass
class WidgetButton(ButtonTypeMixin, ButtonUrlMixin, ButtonConfig):
    button_type = ButtonType.WIDGET
    new_mode: bool = False

    def __iter__(self):
        yield from super().__iter__()
        yield "new_mode", self.new_mode


@dataclass
class HyperlinkButton(ButtonTypeMixin, ButtonUrlMixin, ButtonConfig):
    button_type = ButtonType.HYPERLINK
    target: HyperlinkTarget = HyperlinkTarget.BLANK

    def __iter__(self):
        yield from super().__iter__()
        yield "target", self.target.value


@dataclass
class ActionButton(ButtonTypeMixin, ButtonUrlMixin, ButtonConfig):
    button_type = ButtonType.ACTION
    method: RequestType = RequestType.POST
    action_label: str = ""

    description_fields: str = "<p>Are you sure you want to proceed?</p>"
    instance_display: InstanceDisplay = None
    serializer: Serializer = None
    confirm_config: ButtonConfig = ButtonConfig(label="Confirm", title="Confirm")
    cancel_config: ButtonConfig = ButtonConfig(label="Cancel", title="Cancel")

    identifiers: List[str] = field(default_factory=list)

    def get_fields(self, request: Request) -> Dict:
        fields = dict()
        rs = RepresentationSerializer
        ls = ListSerializer
        field_items = self.serializer().fields.items()

        for name, field in filter(lambda f: not isinstance(f[1], (rs, ls)), field_items):
            fields[name] = field.get_representation(request, name)

        for name, field in filter(lambda f: isinstance(f[1], (rs, ls)), field_items):
            representation = field.get_representation(request, name)
            fields[representation["related_key"]].update(representation)
            del fields[representation["related_key"]]["related_key"]

        return fields

    def _get_fields(self, request: Request) -> Dict:
        fields = self.get_fields(request)
        serializer_class = self.serializer
        return fields

    def __iter__(self):
        yield from super().__iter__()
        yield "action_label", self.action_label
        yield "method", self.method.value

        yield "description_fields", self.description_fields
        yield "confirm_config", dict(self.confirm_config)
        yield "cancel_config", dict(self.cancel_config)

        yield "identifiers", self.identifiers

        if self.instance_display:
            yield "instance_display", list(self.instance_display)

        if self.serializer:
            assert (
                hasattr(self, "request") and self.request is not None
            ), "Action Buttons who define a custom serializer, needs to have access to the request"
            yield "fields", self._get_fields(self.request)

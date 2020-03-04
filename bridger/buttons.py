from collections import defaultdict
from enum import Enum
from typing import Any, List, NamedTuple, Optional, Tuple, Union

from bridger.display import InstanceDisplay
from bridger.enums import Button


class ButtonLevel(Enum):
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    LINK = "link"
    DEFAULT = "default"


class CustomButton(NamedTuple):
    key: Optional[str] = None
    endpoint: Optional[str] = None

    label: Optional[str] = None
    icon: Optional[str] = None
    title: Optional[str] = None

    level: ButtonLevel = ButtonLevel.DEFAULT

    def to_dict(self):
        assert self.label or self.icon, "At least a label or an icon is needed."
        assert self.key or self.endpoint, "At least a key or an endpoint is needed."
        assert self.button_type is not None, "A button type has to be provided."

        rv = defaultdict(dict, {"type": self.button_type, "level": self.level.value})

        fields = ["key", "endpoint", "label", "icon", "title"]

        for field in fields:
            _field = getattr(self, field, None)
            if _field:
                rv[field] = _field

        return rv


class HyperlinkButton(CustomButton):
    button_type = Button.HYPERLINK.value


class WidgetButton(CustomButton):
    button_type = Button.WIDGET.value


class DropdownButton(NamedTuple):
    buttons: List
    label: Optional[str] = None
    icon: Optional[str] = None
    title: Optional[str] = None
    button_type = Button.DROPDOWN.value

    level: ButtonLevel = ButtonLevel.DEFAULT

    def to_dict(self):
        rv = defaultdict(list, {"type": self.button_type, "level": self.level.value})

        for button in self.buttons:
            rv["buttons"].append(button.to_dict())

        if self.label:
            rv["label"] = self.label

        if self.icon:
            rv["icon"] = self.icon

        if self.title:
            rv["title"] = self.title

        return rv


class AdditionalButtonConfig(NamedTuple):
    icon: Optional[str] = None
    label: Optional[str] = None
    title: Optional[str] = None
    level: ButtonLevel = ButtonLevel.DEFAULT

    def to_dict(self):
        rv = dict({"level": self.level.value})

        for field in ["icon", "title", "label"]:
            _field = getattr(self, field, None)
            if _field:
                rv[field] = _field

        return rv


class ActionButton(NamedTuple):
    method: str
    action_label: str

    key: Optional[str] = None
    endpoint: Optional[str] = None

    label: Optional[str] = None
    icon: Optional[str] = None
    title: Optional[str] = None

    description_fields: List[str] = []
    instance_display: Optional[InstanceDisplay] = None
    confirm_config: Optional[AdditionalButtonConfig] = None
    cancel_config: Optional[AdditionalButtonConfig] = None

    identifiers: List[str] = None

    button_type = Button.ACTION.value

    def to_dict(self):
        assert bool(self.key) != bool(
            self.endpoint
        ), "Either key or endpoint can be defined."
        rv = defaultdict(list, {"type": self.button_type})

        rv["method"] = self.method

        if self.endpoint:
            rv["endpoint"] = self.endpoint

        if self.key:
            rv["key"] = self.key

        rv["action_label"] = self.action_label

        rv["description_fields"] = self.description_fields
        if self.instance_display:
            rv["form_display"] = self.instance_display.to_dict()
        else:
            rv["form_display"] = []

        if self.label:
            rv["label"] = self.label

        if self.icon:
            rv["icon"] = self.icon

        if self.title:
            rv["title"] = self.title

        if self.confirm_config:
            rv["confirm_config"] = self.confirm_config.to_dict()

        if self.cancel_config:
            rv["cancel_config"] = self.cancel_config.to_dict()

        if self.identifiers is not None:
            rv["identifiers"] = self.identifiers

        return rv

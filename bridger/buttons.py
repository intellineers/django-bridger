from collections import defaultdict
from typing import Any, List, NamedTuple, Optional, Tuple, Union

from bridger.display import InstanceDisplay
from bridger.enums import Button


class CustomButton(NamedTuple):
    key: str
    label: Optional[str] = None
    icon: Optional[str] = None
    title: Optional[str] = None

    def to_dict(self):
        assert self.label or self.icon, "At least a label or an icon is needed."

        rv = defaultdict(dict, {"type": self.button_type, "key": self.key})

        if self.label:
            rv["label"] = self.label

        if self.icon:
            rv["icon"] = self.icon

        if self.title:
            rv["title"] = self.title

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

    def to_dict(self):
        rv = defaultdict(list, {"type": self.button_type})

        for button in self.buttons:
            rv["buttons"].append(button.to_dict())

        if self.label:
            rv["label"] = self.label

        if self.icon:
            rv["icon"] = self.icon

        if self.title:
            rv["title"] = self.title

        return rv


class ActionButton(NamedTuple):
    method: str
    action_label: str

    key: Optional[str] = None
    endpoint: Optional[str] = None

    description_fields: List[str] = []
    instance_display: Optional[InstanceDisplay] = None

    label: Optional[str] = None
    icon: Optional[str] = None
    title: Optional[str] = None

    confirm_label: Optional[str] = None
    cancel_label: Optional[str] = None

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

        rv["descriptions_fields"] = self.description_fields
        if self.instance_display:
            rv["form_display"] = self.instance_display.to_dict()

        if self.label:
            rv["label"] = self.label

        if self.icon:
            rv["icon"] = self.icon

        if self.title:
            rv["title"] = self.title

        if self.confirm_label:
            rv["confirm_label"] = self.confirm_label

        if self.cancel_label:
            rv["cancel_label"] = self.cancel_label

        return rv

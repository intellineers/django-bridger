from collections import defaultdict
from typing import List, NamedTuple, Optional, Union, Tuple, Any

from bridger.enums import Button


class CustomButton(NamedTuple):
    key: str
    label: Optional[str] = None
    icon: Optional[str] = None
    title: Optional[str] = None

    def to_dict(self):
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


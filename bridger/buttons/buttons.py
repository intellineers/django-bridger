from dataclasses import dataclass, field
from typing import Any, List, Optional

from bridger.display import InstanceDisplay
from bridger.enums import RequestType

from .bases import ButtonConfig, ButtonTypeMixin, ButtonUrlMixin
from .enums import ButtonType, HyperlinkTarget


@dataclass
class DropDownButton(ButtonTypeMixin, ButtonConfig):
    button_type = ButtonType.DROPDOWN
    buttons: List = field(default_factory=list)

    def __iter__(self):
        yield from super().__iter__()
        yield "buttons", [dict(button) for button in self.buttons]


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
    confirm_config: ButtonConfig = ButtonConfig(label="Confirm", title="Confirm")
    cancel_config: ButtonConfig = ButtonConfig(label="Cancel", title="Cancel")

    identifiers: List[str] = field(default_factory=list)

    # TODO: Not functional yet
    fields: Any = None

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

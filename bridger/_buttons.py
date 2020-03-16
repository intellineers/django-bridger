from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import List, Optional


class ButtonLevel(Enum):
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    LINK = "link"
    DEFAULT = "default"


class ButtonType(Enum):

    # Buttons
    REFRESH = "refresh"
    NEW = "new"
    DELETE = "delete"

    # Buttons and Create Buttons
    SAVE = "save"
    SAVE_AND_CLOSE = "saveandclose"
    SAVE_AND_NEW = "saveandnew"

    # Create Buttons
    RESET = "reset"

    # Custom Buttons
    DROPDOWN = "dropdown"
    HYPERLINK = "hyperlink"
    WIDGET = "widget"
    ACTION = "action"

    @classmethod
    def buttons(cls):
        return [
            cls.REFRESH.value,
            cls.NEW.value,
            cls.DELETE.value,
            cls.SAVE.value,
            cls.SAVE_AND_CLOSE.value,
            cls.SAVE_AND_NEW.value,
        ]

    @classmethod
    def create_buttons(cls):
        return [
            cls.SAVE.value,
            cls.SAVE_AND_CLOSE.value,
            cls.SAVE_AND_NEW.value,
            cls.RESET.value,
        ]

    @classmethod
    def custom_buttons(cls):
        return [
            cls.DROPDOWN.value,
            cls.HYPERLINK.value,
            cls.WIDGET.value,
            cls.ACTION.value,
        ]


@dataclass
class CustomButton:
    error_messages = {
        "xor_key_endpoint": "Either key or endpoint has to be defined.",
        "or_label_icon": "Either label or icon has to be defined.",
        "exists_button_type": "The field button_type has to exist.",
    }

    level: ButtonLevel = ButtonLevel.DEFAULT

    key: Optional[str] = None
    endpoint: Optional[str] = None
    label: Optional[str] = None
    icon: Optional[str] = None
    title: Optional[str] = None

    def __post_init__(self):
        assert bool(self.key) != bool(self.endpoint), self.error_messages[
            "xor_key_endpoint"
        ]
        assert self.label or self.icon, self.error_messages["or_label_icon"]
        assert hasattr(self, "button_type"), self.error_messages["exists_button_type"]

    # def __dict__(self):
    #     return super().__dict__

    def __iter__(self):
        for field_key in ["key", "endpoint", "label", "icon", "title"]:
            value = getattr(self, field_key, None)
            if value:
                yield field_key, value

        yield "type", self.button_type.value


@dataclass
class HyperlinkButton(CustomButton):
    button_type: ButtonType = ButtonType.HYPERLINK


@dataclass
class WidgetButton(CustomButton):
    button_type = ButtonType.WIDGET


@dataclass
class DropDownButton(CustomButton):
    button_type = ButtonType.DROPDOWN
    buttons: List[CustomButton] = field(default_factory=list)

    def __post_init__(self):
        assert not self.key and not self.endpoint
        assert self.label or self.icon, self.error_messages["or_label_icon"]
        assert hasattr(self, "button_type"), self.error_messages["exists_button_type"]

    def __iter__(self):
        yield from super().__iter__()
        yield "buttons", [dict(button) for button in self.buttons]


btn = DropDownButton(label="A", icon="B", buttons=[HyperlinkButton(key="A", icon="B")])

print(dict(btn))

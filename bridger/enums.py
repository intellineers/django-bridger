from enum import Enum
from typing import Union


class Button(Enum):

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


class WidgetType(Enum):
    LIST = "list"
    INSTANCE = "instance"
    CHART = "chart"


class Operator(Enum):
    EQUAL = "=="
    UNEQUAL = "!="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="


class Unit(Enum):
    FRACTION = "fr"
    REM = "rem"
    PIXEL = "px"

    def __call__(self, _value):
        return (_value, self.value)

    def unit(self, _value: Union[float, str, int]):
        assert isinstance(
            _value, (float, str, int)
        ), f"_value needs to be one of str, float or int"

        return f"{float(_value)}{self.value}"


class AuthType(Enum):
    NONE = "NONE"
    JWT = "JWT"

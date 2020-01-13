from typing import Union

from enum import Enum


class Button(Enum):
    # List and Instance
    REFRESH = "refresh"
    RESET = "reset"
    NEW = "new"
    DELETE = "delete"

    # Instance
    SAVE = "save"
    SAVE_AND_CLOSE = "saveandclose"
    SAVE_AND_NEW = "saveandnew"

    # Custom
    DROPDOWN = "dropdown"
    HYPERLINK = "hyperlink"
    WIDGET = "widget"
    ACTION = "action"


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

    def unit(self, _value: Union[float, str, int]):
        assert isinstance(
            _value, (float, str, int)
        ), f"_value needs to be one of str, float or int"

        return f"{float(_value)}{self.value}"


class AuthType(Enum):
    NONE = "NONE"
    JWT = "JWT"

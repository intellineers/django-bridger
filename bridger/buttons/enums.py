from enum import Enum


class ButtonLevel(Enum):
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    LINK = "link"
    DEFAULT = "default"


class ButtonType(Enum):
    DROPDOWN = "dropdown"
    HYPERLINK = "hyperlink"
    WIDGET = "widget"
    ACTION = "action"


class HyperlinkTarget(Enum):
    BLANK = "_blank"
    SELF = "_self"
    PARENT = "_parent"
    TOP = "_top"

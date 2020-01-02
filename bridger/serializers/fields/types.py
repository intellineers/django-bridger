from enum import Enum


class BridgerType(Enum):
    TEXT = "text"
    TEXTEDITOR = "texteditor"
    NUMBER = "number"
    DATETIME = "datetime"
    DATE = "date"
    TIME = "time"
    PRIMARY_KEY = "primary_key"
    BOOLEAN = "boolean"
    SELECT = "select"
    IMAGE = "image"
    FILE = "file"
    LIST = "list"
    PERCENT = "percent"
    JSON = "json"


class ReturnContentType(Enum):
    HTML = "html"
    JSON = "json"

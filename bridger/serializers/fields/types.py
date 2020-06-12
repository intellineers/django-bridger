from enum import Enum


class BridgerType(Enum):
    TEXT = "text"
    TEXTEDITOR = "texteditor"
    MARKDOWNEDITOR = "markdowneditor"
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
    MARKDOWN = "markdown"

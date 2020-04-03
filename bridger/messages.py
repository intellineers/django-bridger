from dataclasses import dataclass
from enum import Enum


class MessageType(Enum):
    INFO = "info"
    WARNING = "warning"
    SUCCESS = "success"
    ERROR = "error"


@dataclass
class Message:
    message: str
    message_type: MessageType = MessageType.INFO
    autoclose: int = None

    def __iter__(self):
        yield "message", self.message
        yield "type", self.message_type.value
        if self.autoclose:
            yield "autoclose", self.autoclose * 1000


def info(message, **kwargs):
    return Message(message=message, message_type=MessageType.INFO, **kwargs)


def warning(message, **kwargs):
    return Message(message=message, message_type=MessageType.WARNING, **kwargs)


def success(message, **kwargs):
    return Message(message=message, message_type=MessageType.SUCCESS, **kwargs)


def error(message, **kwargs):
    return Message(message=message, message_type=MessageType.ERROR, **kwargs)

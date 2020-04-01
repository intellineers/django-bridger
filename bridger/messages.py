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

    def __iter__(self):
        yield "message", self.message
        yield "type", self.message_type.value


def info(message):
    return Message(message=message, message_type=MessageType.INFO)

def warning(message):
    return Message(message=message, message_type=MessageType.WARNING)

def success(message):
    return Message(message=message, message_type=MessageType.SUCCESS)

def error(message):
    return Message(message=message, message_type=MessageType.ERROR)
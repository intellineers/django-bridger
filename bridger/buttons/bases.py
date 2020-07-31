from dataclasses import dataclass
from typing import Optional

from .enums import ButtonLevel, ButtonType


@dataclass(unsafe_hash=True)
class ButtonConfig:
    label: Optional[str] = None
    icon: Optional[str] = None
    title: Optional[str] = None

    level: ButtonLevel = ButtonLevel.DEFAULT

    weight: int = 100

    def __post_init__(self):
        if hasattr(super(), "__post_init__"):
            super().__post_init__()

        assert self.label or self.icon, "Either label or icon has to be defined."

    def __iter__(self):
        if hasattr(super(), "__iter__"):
            yield from super().__iter__()

        for key in ["label", "icon", "title"]:
            value = getattr(self, key, None)
            if value:
                yield key, value
        yield "level", self.level.value


@dataclass(unsafe_hash=True)
class ButtonTypeMixin:
    def __post_init__(self):
        if hasattr(super(), "__post_init__"):
            super().__post_init__()

        assert hasattr(self, "button_type"), "button_type cannot be None."

    def __iter__(self):
        if hasattr(super(), "__iter__"):
            yield from super().__iter__()

        yield "type", self.button_type.value


@dataclass(unsafe_hash=True)
class ButtonUrlMixin:
    key: Optional[str] = None
    endpoint: Optional[str] = None

    def __post_init__(self):
        if hasattr(super(), "__post_init__"):
            super().__post_init__()

        assert bool(self.key) != bool(self.endpoint), "Either key or endpoint has to be defined. (Not both)"

    def __iter__(self):
        if hasattr(super(), "__iter__"):
            yield from super().__iter__()

        if self.key:
            yield "key", self.key

        if self.endpoint:
            yield "endpoint", self.endpoint

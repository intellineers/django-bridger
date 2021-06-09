from collections import defaultdict
from typing import Any, Dict, List, NamedTuple, Optional, Tuple, Union

from bridger.serializers import percent_decorator


class BaseField(NamedTuple):
    key: str
    label: str
    decorators: List = None
    help_text: str = None

    def to_dict(self):
        base = {"key": self.key, "label": self.label, "type": self.type}
        if self.decorators:
            base["decorators"] = self.decorators
            
        for _attr in ["help_text", "extra"]:
            attr = getattr(self, _attr, None)
            if attr:
                base[_attr] = attr
        return base


class PKField(BaseField):
    type = "primary_key"


class CharField(BaseField):
    type = "text"


class DateField(BaseField):
    type = "date"


class BooleanField(BaseField):
    type = "boolean"


class FloatField(NamedTuple):
    key: str
    label: str
    precision: int = 2
    percent: bool = False
    decorators: List = None
    type = "number"
    help_text: str = None

    def to_dict(self):
        base = {
            "key": self.key,
            "label": self.label,
            "type": self.type,
            "precision": self.precision,
        }
        if self.help_text:
            base['help_text'] = self.help_text

        if self.percent:
            base["type"] = "percent"

            if not self.decorators:
                base["decorators"] = [percent_decorator]

        if self.decorators:
            base["decorators"] = self.decorators

        return base


class IntegerField(FloatField):
    type = "number"
    precision = 0


class PandasFields(NamedTuple):
    fields: List[BaseField]

    def to_dict(self):
        fields = defaultdict(dict)

        for field in self.fields:
            fields[field.key] = field.to_dict()

        return fields

from collections import defaultdict
from typing import Any, Dict, List, NamedTuple, Optional, Tuple, Union

from bridger.serializers import percent_decorator


class BaseField(NamedTuple):
    key: str
    label: str

    decorators: List = None

    def to_dict(self):
        base = {"key": self.key, "label": self.label, "type": self.type}
        if self.decorators:
            base["decorators"] = self.decorators

        return base


class PKField(BaseField):
    type = "primary_key"


class CharField(BaseField):
    type = "text"


class DateField(BaseField):
    type = "date"


class FloatField(NamedTuple):
    key: str
    label: str
    precision: int = 2
    percent: bool = False
    decorators: List = None
    type = "number"

    def to_dict(self):
        base = {
            "key": self.key,
            "label": self.label,
            "type": self.type,
            "precision": self.precision,
        }

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

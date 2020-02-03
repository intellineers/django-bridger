from collections import defaultdict
from typing import Any, Dict, List, NamedTuple, Optional, Tuple, Union


class BaseField(NamedTuple):
    key: str
    label: str

    def to_dict(self):
        return {"key": self.key, "label": self.label, "type": self.type}


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
    type = "number"

    def to_dict(self):
        return {
            "key": self.key,
            "label": self.label,
            "type": self.type,
            "precision": self.precision,
        }


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

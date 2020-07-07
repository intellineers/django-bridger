from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Union

from bridger.display.formatting import Formatting, FormattingRule


@dataclass
class Field:
    key: str
    label: str
    formatting_rules: List[FormattingRule] = field(default_factory=list)
    width: Tuple[Union[float, str, int], str] = None

    def __iter__(self):
        yield "key", self.key
        yield "label", self.label
        yield "formatting_rules", [dict(rule) for rule in self.formatting_rules]

        if self.width:
            yield "width", self.width


@dataclass
class LegendItem:
    icon: str
    label: str
    value: Optional[str] = None

    def __iter__(self):
        yield "icon", self.icon
        yield "label", self.label

        if self.value:
            yield "value", self.value


@dataclass
class Legend:
    items: List[LegendItem]
    label: str = None
    key: str = None

    def __post_init__(self):
        if self.key:
            # TODO: What if we filter for boolean values, item.value == False, then this won't work anymore
            assert all([bool(item.value) for item in self.items]), "If key is set, all items need to specify a value."

    def __iter__(self):
        if self.label:
            yield "label", self.label

        if self.key:
            yield "key", self.key

        yield "items", [dict(item) for item in self.items]


@dataclass
class ListDisplay:
    fields: List[Field]
    legends: List[Legend] = field(default_factory=list)
    formatting: List[Formatting] = field(default_factory=list)

    def __iter__(self):
        yield "fields", [dict(field) for field in self.fields]
        yield "legends", [dict(legend) for legend in self.legends]
        yield "formatting", [dict(formatting) for formatting in self.formatting]


@dataclass
class Calendar:
    title: str
    start: str
    end: str
    filter_date_gte: str
    filter_date_lte: str

    def __iter__(self):
        yield "calendar", {
            "title": self.title,
            "start": self.start,
            "end": self.end,
            "filter_date_gte": self.filter_date_gte,
            "filter_date_lte": self.filter_date_lte,
        }

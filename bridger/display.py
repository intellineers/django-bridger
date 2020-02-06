from collections import defaultdict
from typing import Any, Dict, List, NamedTuple, Optional, Tuple, Union


class ColumnFormatting(NamedTuple):
    style: Dict
    condition: Optional[Tuple[str, Union[int, float, str]]] = None
    all_columns: bool = False

    def to_dict(self):
        rd = {"style": self.style, "all_columns": self.all_columns}
        if self.condition:
            rd["condition"] = list(self.condition)
        return rd


class RowIconCondition(NamedTuple):
    icon: str
    condition: Optional[Tuple[str, Union[int, float, str]]] = None

    def to_dict(self):
        rd = {"icon": self.icon}
        if self.condition:
            rd["condition"] = list(self.condition)
        return rd


class RowStyleCondition(NamedTuple):
    style: Dict
    condition: Optional[Tuple[str, Union[int, float, str]]] = None

    def to_dict(self):
        rd = {"style": self.style}
        if self.condition:
            rd["condition"] = list(self.condition)
        return rd


class RowFormatting(NamedTuple):
    conditions: List[Union[RowIconCondition, RowStyleCondition]]
    column: Optional[str] = None

    def to_dict(self):
        rd = defaultdict(list)
        if self.column:
            rd["column"] = self.column
        for condition in self.conditions:
            rd["conditions"].append(condition.to_dict())
        return rd


class Field(NamedTuple):
    key: str
    label: str = None
    formatting: List[ColumnFormatting] = []
    col: Tuple[str, str] = None

    def to_dict(self):
        rd = defaultdict(list, {"key": self.key})
        if self.label:
            rd["label"] = self.label

        for formatting in self.formatting:
            rd["formatting"].append(formatting.to_dict())

        if self.col:
            rd["col"] = self.col

        return rd


class LegendItem(NamedTuple):
    icon: str
    label: str
    value: Optional[Any] = None

    def to_dict(self):
        rv = {"icon": self.icon, "label": self.label}
        if self.value:
            rv["value"] = self.value
        return rv


class Legend(NamedTuple):
    items: List[LegendItem]
    label: Optional[str] = None
    key: Optional[str] = None

    def to_dict(self):
        tv = {"items": list()}

        if self.label:
            tv["label"] = self.label
        if self.key:
            tv["key"] = self.key

        for item in self.items:
            tv["items"].append(item.to_dict())

        return tv


class Calender(NamedTuple):
    title: str
    start: str
    end: str

    filter_date_gte: str
    filter_date_lte: str

    def to_dict(self):
        return {
            "title": self.title,
            "start": self.start,
            "end": self.end,
            "filter_date_gte": self.filter_date_gte,
            "filter_date_lte": self.filter_date_lte,
        }


class ListDisplay(NamedTuple):
    fields: List[Field]
    formatting: List[RowFormatting] = []
    legends: List[Legend] = []
    calendar: Calender = None

    def to_dict(self):
        list_display = defaultdict(list)
        for field in self.fields:
            list_display["fields"].append(field.to_dict())

        for formatting in self.formatting:
            list_display["formatting"].append(formatting.to_dict())

        for legend in self.legends:
            list_display["legends"].append(legend.to_dict())

        if self.calendar:
            list_display["calendar"] = self.calendar.to_dict()

        return list_display


class FieldSet(NamedTuple):
    # This should include the recursive subtypes, but then mypy gets a recursion error
    fields: List

    def to_dict(self):
        rl = list()
        for field in self.fields:
            if isinstance(field, str):
                rl.append(field)
            else:
                rl.append(field.to_dict())
        return rl


class SectionList(NamedTuple):
    key: str

    def to_dict(self):
        return {"key": self.key}


class Section(NamedTuple):
    fields: FieldSet = None
    section_list: SectionList = None

    title: Optional[str] = None
    collapsed: bool = False

    def to_dict(self):
        rd = {}

        if self.fields:
            rd["fields"] = self.fields.to_dict()
        elif self.section_list:
            rd["list"] = self.section_list.to_dict()

        if self.title:
            rd["title"] = self.title

        if self.collapsed:
            rd["collapsed"] = self.collapsed

        return rd


class InstanceDisplay(NamedTuple):
    sections: List[Section]

    def to_dict(self):
        instance_display = list()
        for section in self.sections:
            instance_display.append(section.to_dict())
        return instance_display


# import json
# from pprint import pprint
# from bridger.enums import Operator

# i = InstanceDisplay(
#     sections=[
#         Section(fields=FieldSet(["a1", "a2", FieldSet(["a31", "a32"])])),
#         Section(
#             title="Section2",
#             collapsed=True,
#             fields=FieldSet(
#                 ["b1", "b2", FieldSet(["b31", FieldSet(["b311", "b312"])])]
#             ),
#         ),
#     ]
# )
# pprint(json.loads(json.dumps(i.to_dict())))

# l = ListDisplay(
#     fields=[
#         Field(key="title", label="Title"),
#         Field(
#             key="title",
#             label="Title",
#             formatting=[
#                 ColumnFormatting(style="bold", condition=(Operator.GREATER.value, 3))
#             ],
#         ),
#         Field(key="title", label="Title"),
#     ],
#     formatting=[
#         RowFormatting(
#             column="title",
#             conditions=[
#                 RowIconCondition(
#                     icon="wb-icon-something", condition=(Operator.EQUAL.value, "abc")
#                 ),
#                 RowStyleCondition(
#                     style="bold", condition=(Operator.UNEQUAL.value, "abc")
#                 ),
#             ],
#         )
#     ],
# )
# pprint(json.loads(json.dumps(l.to_dict())))

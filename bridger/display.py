from collections import defaultdict
from typing import List, NamedTuple, Optional, Union, Tuple, Any, Dict


class ColumnFormatting(NamedTuple):
    style: str
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
    column: str
    conditions: List[Union[RowIconCondition, RowStyleCondition]]

    def to_dict(self):
        rd = defaultdict(list, {"column": self.column})
        for condition in self.conditions:
            rd["conditions"].append(condition.to_dict())
        return rd


class Field(NamedTuple):
    key: str
    label: str
    formatting: List[ColumnFormatting] = []

    def to_dict(self):
        rd = defaultdict(list, {"key": self.key, "label": self.label})
        for formatting in self.formatting:
            rd["formatting"].append(formatting.to_dict())
        return rd


class LegendItem(NamedTuple):
    icon: str
    label: str
    value: Optional[Any] = None

    def to_dict(self):
        rv = {"icon": self.icon, "label": self.label}
        if self.value:
            tv["value"] = self.value
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


class ListDisplay(NamedTuple):
    fields: List[Field]
    formatting: List[RowFormatting] = []
    legends: List[Legend] = []

    def to_dict(self):
        list_display = defaultdict(list)
        for field in self.fields:
            list_display["fields"].append(field.to_dict())

        for formatting in self.formatting:
            list_display["formatting"].append(formatting.to_dict())

        for legend in self.legends:
            list_display["legends"].append(legend.to_dict())

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


class Section(NamedTuple):
    fields: FieldSet
    title: Optional[str] = None
    collapsed: bool = False

    def to_dict(self):
        rd = {"fields": self.fields.to_dict()}

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

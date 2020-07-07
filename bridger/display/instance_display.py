from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class FieldSet:
    fields: List

    def __post_init__(self):
        assert isinstance(self.fields[0], (str, FieldSet)), "fields can only contain strings or more FieldSets."

    def __iter__(self):
        for field in self.fields:
            if isinstance(field, str):
                yield field
            else:
                yield list(field)


@dataclass
class SectionList:
    key: str

    def __iter__(self):
        yield "key", self.key


@dataclass
class Section:
    fields: FieldSet = None
    section_list: SectionList = None
    title: str = None
    collapsed: bool = False

    def __post_init__(self):
        assert bool(self.fields) != bool(self.section_list), "Either fields have to be provided or section_list, not both."

    def __iter__(self):
        if self.fields:
            yield "fields", [field for field in self.fields]
        elif self.section_list:
            yield "list", dict(self.section_list)

        yield "collapsed", self.collapsed

        if self.title:
            yield "title", self.title


@dataclass
class InstanceDisplay:
    sections: List[Section]

    def __iter__(self):
        yield from [dict(section) for section in self.sections]

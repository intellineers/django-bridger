from dataclasses import dataclass
from typing import List, Tuple


@dataclass(unsafe_hash=True)
class FieldSet:
    fields: Tuple

    def __post_init__(self):
        assert isinstance(self.fields[0], (str, FieldSet)), "fields can only contain strings or more FieldSets."
        assert isinstance(self.fields, tuple), f"fields have to be a tuple, not {type(self.fields)}"

    def __iter__(self):
        for field in self.fields:
            if isinstance(field, str):
                yield field
            else:
                yield tuple(field)


@dataclass(unsafe_hash=True)
class SectionList:
    key: str

    def __iter__(self):
        yield "key", self.key


@dataclass(unsafe_hash=True)
class Section:
    fields: FieldSet = None
    section_list: SectionList = None
    title: str = None
    collapsed: bool = False

    def __post_init__(self):
        assert bool(self.fields) != bool(self.section_list), "Either fields have to be provided or section_list, not both."

    def __iter__(self):
        if self.fields:
            yield "fields", tuple(field for field in self.fields)
        elif self.section_list:
            yield "list", dict(self.section_list)

        yield "collapsed", self.collapsed

        if self.title:
            yield "title", self.title


@dataclass(unsafe_hash=True)
class InstanceDisplay:
    sections: Tuple[Section]

    def __post_init__(self):
        assert isinstance(self.sections, tuple), f"sections have to be a tuple, not {type(self.sections)}"

    def __iter__(self):
        # All sections need to be iterated over and be converted into a dict
        for section in self.sections:
            yield dict(section)

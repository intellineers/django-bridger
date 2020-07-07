from dataclasses import dataclass
from typing import Dict, List, Union

from bridger.enums import Operator


@dataclass
class Condition:
    operator: Operator
    value: Union[str, float, int, bool]

    def __post_init__(self):
        if self.operator == Operator.EXISTS:
            assert isinstance(self.value, bool), f"{Operator.EXISTS.value} is only compatible with bool"


@dataclass
class FormattingRule:
    icon: str = None
    style: Dict = None
    condition: Condition = None

    def __post_init__(self):
        assert self.icon or self.style, "icon and style cannot both be None."

    def __iter__(self):
        yield "icon", self.icon
        yield "style", self.style
        if self.condition:
            if isinstance(self.condition, tuple):
                yield "condition", self.condition
            else:
                yield "condition", (self.condition.operator.value, self.condition.value)


@dataclass
class Formatting:
    formatting_rules: List[FormattingRule]
    column: str = None

    def __post_init__(self):
        if self.column is None:
            assert all(
                [not bool(rule.condition) for rule in self.formatting_rules]
            ), "Specifying conditions, without a reference column is not possible."

    def __iter__(self):
        yield "column", self.column
        yield "formatting_rules", [dict(rule) for rule in self.formatting_rules]

from collections import defaultdict
from typing import List, NamedTuple, Optional

from bridger.display import InstanceDisplay
from bridger.enums import Button


class FSMButton(NamedTuple):
    action_label: str
    key: str

    description_fields: List[str] = []
    instance_display: Optional[InstanceDisplay] = None

    label: Optional[str] = None
    icon: Optional[str] = None
    title: Optional[str] = None

    confirm_label: Optional[str] = None
    cancel_label: Optional[str] = None

    method = "PATCH"
    button_type = Button.ACTION.value

    def to_dict(self):
        rv = defaultdict(list, {"type": self.button_type})

        rv["method"] = self.method
        rv["action_label"] = self.action_label
        rv["key"] = self.key

        rv["descriptions_fields"] = self.description_fields
        if self.instance_display:
            rv["form_display"] = self.instance_display.to_dict()

        if self.label:
            rv["label"] = self.label

        if self.icon:
            rv["icon"] = self.icon

        if self.title:
            rv["title"] = self.title

        if self.confirm_label:
            rv["confirm_label"] = self.confirm_label

        if self.cancel_label:
            rv["cancel_label"] = self.cancel_label

        return rv

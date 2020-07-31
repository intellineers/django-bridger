from contextlib import suppress
from typing import List, Set, Dict

from rest_framework.request import Request

from bridger.enums import Button
from bridger.metadata.mixins import BridgerViewSetConfig

class BaseButtonConfig:

    FSM_LIST = True
    FSM_INSTANCE = True
    FSM_DROPDOWN = False
    FSM_WEIGHT = 100
    FSM_BUTTONS = set()

    LIST_BUTTONS = {Button.NEW.value, Button.REFRESH.value}
    LIST_BUTTONS_ORDERING = [Button.NEW.value, Button.REFRESH.value]

    INSTANCE_BUTTONS = {Button.SAVE.value, Button.REFRESH.value, Button.DELETE.value}
    INSTANCE_BUTTONS_ORDERING = [Button.SAVE.value, Button.REFRESH.value, Button.DELETE.value]

    CREATE_BUTTONS = {Button.SAVE.value, Button.SAVE_AND_CLOSE.value, Button.SAVE_AND_NEW.value, Button.RESET.value}
    CREATE_BUTTONS_ORDERING = [Button.SAVE.value, Button.SAVE_AND_CLOSE.value, Button.SAVE_AND_NEW.value, Button.RESET.value]

    CUSTOM_INSTANCE_BUTTONS = set()
    CUSTOM_LIST_INSTANCE_BUTTONS = set()
    CUSTOM_BUTTONS = set()

    def get_custom_instance_buttons(self, request: Request) -> List:
        return []

    def get_list_instance_buttons(self, request: Request) -> List:
        return []

    def order_buttons(self, buttons: Set, ordering: List) -> List:
        yield from filter(lambda b: b in buttons, ordering)

    def get_list_buttons(self, request: Request) -> List:
        content_type = self.viewset.get_content_type()
        add_permission = f"{content_type.app_label}.add_{content_type.model}"

        if not request.user.has_perm(add_permission):
            with suppress(KeyError):
                self.LIST_BUTTONS.remove(Button.NEW.value)

        yield from self.order_buttons(self.LIST_BUTTONS, self.LIST_BUTTONS_ORDERING)

    def get_instance_buttons(self, request: Request) -> List:
        content_type = self.viewset.get_content_type()
        change_permission = f"{content_type.app_label}.change_{content_type.model}"
        delete_permission = f"{content_type.app_label}.delete_{content_type.model}"

        if not request.user.has_perm(change_permission):
            with suppress(KeyError):
                self.INSTANCE_BUTTONS.remove(Button.SAVE.value)

        if not request.user.has_perm(delete_permission):
            with suppress(KeyError):
                self.INSTANCE_BUTTONS.remove(Button.DELETE.value)

        yield from self.order_buttons(self.INSTANCE_BUTTONS, self.INSTANCE_BUTTONS_ORDERING)

    def get_create_buttons(self, request: Request) -> List:
        yield from self.order_buttons(self.CREATE_BUTTONS, self.CREATE_BUTTONS_ORDERING)

    def to_metadata(self, request: Request) -> Dict:
        yield "instance", self.get_instance_buttons(request)
        yield "list", self.get_list_buttons(request)
        yield "create", self.get_create_buttons(request)
        yield "custom_instance", self.get_custom_instance_buttons(request)

    def determine_metadata(self) -> Dict:
        return {"buttons": self.to_metadata()}


class ButtonViewSetMixin:
    button_config_class = BaseButtonConfig

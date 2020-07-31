from contextlib import suppress
from typing import List, Set, Dict

from rest_framework.request import Request

from bridger.enums import Button
from bridger.metadata.mixins import BridgerViewSetConfig
from bridger.signals.instance_buttons import add_instance_button

class ButtonConfig(BridgerViewSetConfig):

    # Utils
    def order_buttons(self, buttons: Set, ordering: List) -> List:
        yield from filter(lambda b: b in buttons, ordering)

    # FSM Button Configuration
    FSM_LIST = True
    FSM_INSTANCE = True
    FSM_DROPDOWN = False
    FSM_WEIGHT = 100
    FSM_BUTTONS = set()

    # List Button Configuration
    LIST_BUTTONS = {Button.NEW.value, Button.REFRESH.value}
    LIST_BUTTONS_ORDERING = [Button.NEW.value, Button.REFRESH.value]

    def get_list_buttons(self) -> List:
        content_type = self.view.get_content_type()
        add_permission = f"{content_type.app_label}.add_{content_type.model}"

        if not self.request.user.has_perm(add_permission):
            with suppress(KeyError):
                self.LIST_BUTTONS.remove(Button.NEW.value)

        yield from self.order_buttons(self.LIST_BUTTONS, self.LIST_BUTTONS_ORDERING)

    # Instance Button Configuration
    INSTANCE_BUTTONS = {Button.SAVE.value, Button.REFRESH.value, Button.DELETE.value}
    INSTANCE_BUTTONS_ORDERING = [Button.SAVE.value, Button.REFRESH.value, Button.DELETE.value]

    def get_instance_buttons(self) -> List:
        content_type = self.view.get_content_type()
        change_permission = f"{content_type.app_label}.change_{content_type.model}"
        delete_permission = f"{content_type.app_label}.delete_{content_type.model}"

        if not self.request.user.has_perm(change_permission):
            with suppress(KeyError):
                self.INSTANCE_BUTTONS.remove(Button.SAVE.value)

        if not self.request.user.has_perm(delete_permission):
            with suppress(KeyError):
                self.INSTANCE_BUTTONS.remove(Button.DELETE.value)

        yield from self.order_buttons(self.INSTANCE_BUTTONS, self.INSTANCE_BUTTONS_ORDERING)

    # Create Button Configuration
    CREATE_BUTTONS = {Button.SAVE.value, Button.SAVE_AND_CLOSE.value, Button.SAVE_AND_NEW.value, Button.RESET.value}
    CREATE_BUTTONS_ORDERING = [Button.SAVE.value, Button.SAVE_AND_CLOSE.value, Button.SAVE_AND_NEW.value, Button.RESET.value]

    def get_create_buttons(self) -> List:
        yield from self.order_buttons(self.CREATE_BUTTONS, self.CREATE_BUTTONS_ORDERING)

    # Custom Instance Button Configuration
    CUSTOM_INSTANCE_BUTTONS = set()
    CUSTOM_LIST_INSTANCE_BUTTONS = set()

    def get_custom_instance_buttons(self) -> Set:
        return self.CUSTOM_INSTANCE_BUTTONS

    def get_custom_list_instance_buttons(self) -> Set:
        return self.CUSTOM_LIST_INSTANCE_BUTTONS

    def _get_custom_instance_buttons(self):
        custom_instance_buttons = set()
        if self.instance:
            custom_instance_buttons |= self.get_custom_instance_buttons()
            if self.FSM_INSTANCE:
                custom_instance_buttons |= self.FSM_BUTTONS

        else:
            custom_instance_buttons |= self.get_custom_list_instance_buttons()
            if self.FSM_LIST:
                custom_instance_buttons |= self.FSM_BUTTONS

        # custom_instance_buttons |= add_instance_button.send(self.__class__, many=not self.instance)

        return sorted(
            custom_instance_buttons,
            key=lambda element: element.weight
        )


    # Custom Button Configuration
    CUSTOM_BUTTONS = set()

    def get_metadata(self) -> Dict:
        if self.instance:
            yield "instance", self.get_instance_buttons()
        else:
            yield "list", self.get_list_buttons()
            yield "create", self.get_create_buttons()

        yield "custom_instance", self._get_custom_instance_buttons()

    @classmethod
    def get_metadata_key(cls):
        return "buttons"

    @classmethod
    def get_metadata_fieldname(cls):
        return "button_config_class"

class ButtonConfigMixin:
    button_config_class = ButtonConfig

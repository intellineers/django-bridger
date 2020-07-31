from bridger import buttons as bt
from bridger import display as dp

from bridger.buttons.metadata_config import ButtonConfig

from tests.serializers import ActionButtonSerializer


class RelatedModelTestButtonConfig(ButtonConfig):
    FSM_DROPDOWN = True
    CUSTOM_INSTANCE_BUTTONS = CUSTOM_LIST_INSTANCE_BUTTONS = {
        bt.DropDownButton(
            label="Dropdown",
            icon="wb-icon-triangle-down",
            buttons=(
                bt.DropDownButton(
                    label="Dropdown",
                    icon="wb-icon-triangle-down",
                    buttons=(
                        bt.ActionButton(
                            label="TestButton",
                            icon="wb-icon-trash",
                            endpoint="http://localhost:5000/relatedmodeltest/",
                            instance_display=dp.InstanceDisplay(
                                sections=(
                                    dp.Section(
                                        fields=dp.FieldSet(fields=("char_field", "custom_field"))
                                    ),
                                )
                            ),
                            serializer=ActionButtonSerializer,
                        ),
                    ),
                ),
            ),
        ),
        bt.HyperlinkButton(key="html", icon="wb-icon-trash", label="Authenticated Subpage", weight=1000),
    }

from typing import Optional

from bridger import display as dp
from bridger.display.metadata_config import DisplayConfig
from bridger.utils.icons import WBIcon

class NotificationDisplayConfig(DisplayConfig):

    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=(
                dp.Field(key="title", label="Title"),
                dp.Field(key="timestamp_created", label="Created"),
                dp.Field(key="message", label="Message"),
            ),
            formatting=[
                dp.Formatting(
                    column="timestamp_read", formatting_rules=[dp.FormattingRule(icon=WBIcon.EYE.value, condition=("∃", True)),],
                ),
            ],
        )

    def get_instance_display(self) -> Optional[dp.InstanceDisplay]:
        return dp.InstanceDisplay(
            sections=(
                dp.Section(
                    fields=dp.FieldSet(
                        fields=(
                            dp.FieldSet(fields=("timestamp_created", "timestamp_received")),
                            dp.FieldSet(fields=("timestamp_received", "timestamp_mailed")),
                            "title",
                            "message",
                        )
                    )
                ),
            )
        )

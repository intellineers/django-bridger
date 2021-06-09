from bridger.display.metadata_config import DisplayConfig
from bridger import display as dp
from typing import Optional
from bridger.utils.colors import WBColor
from bridger.enums import Button, Operator, Unit, WBIcon

class ClubHouseDisplayConfig(DisplayConfig):
   
    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="id", label="Identifier", width=Unit.FRACTION(1)),
                dp.Field(key="created_at", label="Created", width=Unit.FRACTION(1)),
                dp.Field(key="name", label="Name", width=Unit.FRACTION(8)),
            ],
            formatting=[
                dp.Formatting(
                    column="story_type",
                    formatting_rules=[
                        dp.FormattingRule(icon=WBIcon.BOLD.value, condition=dp.Condition(operator=Operator.EQUAL, value="bug"),),
                        dp.FormattingRule(
                            icon=WBIcon.DATA.value, condition=dp.Condition(operator=Operator.EQUAL, value="feature"),
                        ),
                    ],
                ),
                dp.Formatting(
                    column="completed",
                    formatting_rules=[
                        dp.FormattingRule(style={"backgroundColor": "#228B22"}, condition=dp.Condition(Operator.EQUAL, value=True),)
                    ],
                ),
            ],
            legends=[
                dp.Legend(
                    items=[
                        dp.LegendItem(icon=WBIcon.BOLD.value, label="Bug"),
                        dp.LegendItem(icon=WBIcon.DATA.value, label="Feature"),
                    ]
                )
            ],
        )

    def get_instance_display(self) -> Optional[dp.InstanceDisplay]:
        return dp.InstanceDisplay(sections=(dp.Section(fields=dp.FieldSet(("name", "story_type", "description"))),))
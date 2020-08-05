from typing import Optional

from bridger import display as dp
from bridger.display.metadata_config import DisplayConfig
from rest_framework.request import Request
from bridger.enums import Operator, Unit


class ModelTestCalendarDisplayConfig(DisplayConfig):

    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.Calendar(
            title="char_field", start="datetime_field", end="datetime_field1", filter_date_gte="start", filter_date_lte="end",
        )


class ModelTestDisplayConfig(DisplayConfig):
   
    def get_instance_display(self) -> Optional[dp.InstanceDisplay]:
        return dp.InstanceDisplay(
        sections=[
            dp.Section(
                fields=dp.FieldSet(
                    fields=[
                        dp.FieldSet(fields=["image_field", ["char_field", ["integer_field", "float_field"]],]),
                        "tags",
                        "text_field",
                        "percent_field",
                        "decimal_field",
                        "datetime_field",
                        "datetime_field1",
                        "date_field",
                        "time_field",
                        "boolean_field",
                        "choice_field",
                        "status_field",
                        "file_field",
                        "star_rating",
                    ]
                )
            ),
            dp.Section(title="Related Models", section_list=dp.SectionList(key="related_model")),
        ]
    )

    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="tags", label="Tags"),
                dp.Field(key="char_field", label="Char"),
                dp.Field(key="annotated_char_field", label="A-Char"),
                dp.Field(
                    key="float_field",
                    label="Float",
                    formatting_rules=[
                        dp.FormattingRule(icon="wb-icon-trash", condition=dp.Condition(operator=Operator.LESS, value=0),)
                    ],
                ),
                dp.Field(key="percent_field", label="Percent"),
                dp.Field(key="decimal_field", label="Decimal"),
                dp.Field(key="datetime_field", label="DateTime"),
                dp.Field(key="date_field", label="Date"),
                dp.Field(key="time_field", label="Time"),
                dp.Field(
                    key="boolean_field",
                    label="Boolean",
                    formatting_rules=[
                        dp.FormattingRule(style={"color": "red"}, condition=dp.Condition(operator=Operator.EQUAL, value=True),)
                    ],
                ),
                dp.Field(key="choice_field", label="Choice"),
                dp.Field(key="status_field", label="Status"),
                dp.Field(key="image_field", label="Image"),
                dp.Field(key="related_models", label="Related"),
                dp.Field(key="file_field", label="File"),
                dp.Field(key="star_rating", label="Star"),
            ],
            legends=[
                dp.Legend(items=[dp.LegendItem(icon="wb-icon-thumbs-up-full", label="Good Stuff")]),
                dp.Legend(
                    key="status_field",
                    items=[
                        dp.LegendItem(icon="wb-icon-thumbs-up-full", label="Status1", value="status1"),
                        dp.LegendItem(icon="wb-icon-thumbs-up-full", label="Status2", value="status2"),
                        dp.LegendItem(icon="wb-icon-thumbs-up-full", label="Status3", value="status3"),
                    ],
                ),
            ],
            formatting=[
                dp.Formatting(
                    column="integer_field",
                    formatting_rules=[
                        dp.FormattingRule(icon="wb-icon-thumbs-up-full", condition=("<", 5000)),
                        dp.FormattingRule(style={"backgroundColor": "rgb(80,220,100)"}, condition=("<", 5000),),
                    ],
                ),
            ],
        )

from django.db.models import Avg, F, Max, Sum

from bridger import buttons as bt
from bridger import display as dp
from bridger.messages import info
from bridger.enums import Operator, Unit
from bridger.serializers import ListSerializer
from bridger.viewsets import ModelViewSet, RepresentationModelViewSet

from tests.filters import ModelTestFilterSet
from tests.models import ModelTest
from tests.serializers import (
    ModelTestRepresentationSerializer,
    ModelTestSerializer,
)


class ModelTestRepresentationViewSet(RepresentationModelViewSet):
    queryset = ModelTest.objects.all()
    serializer_class = ModelTestRepresentationSerializer

    search_fields = ["char_field"]


class ModelTestModelViewSet(ModelViewSet):
    ENDPOINT = "modeltest-list"
    LIST_DOCS = "tests/endpoint_documentation/model_test.md"
    INSTANCE_DOCS = "# Instance Doc\n"
    INSTANCE_WIDGET_TITLE = "{{char_field}}"
    LIST_WIDGET_TITLE = "List"
    CREATE_WIDGET_TITLE = "Create"

    PREVIEW_TYPE = "instance_display"
    PREVIEW_DISPLAY = dp.InstanceDisplay(
        sections=[dp.Section(fields=dp.FieldSet(fields=["image_field", "char_field"]))]
    )
    PREVIEW_BUTTONS = [
        bt.HyperlinkButton(endpoint="https://www.google.com", label="Open Google"),
        bt.HyperlinkButton(endpoint="https://www.nytimes.com", label="Open NYTimes"),
        bt.WidgetButton(key="self_endpoint", icon="wb-icon-data"),
    ]

    LIST_DISPLAY = dp.ListDisplay(
        fields=[
            dp.Field(key="char_field", label="Char"),
            dp.Field(key="annotated_char_field", label="A-Char"),
            dp.Field(key="integer_field", label="Integer"),
            dp.Field(
                key="float_field",
                label="Float",
                formatting_rules=[
                    dp.FormattingRule(
                        icon="wb-icon-trash",
                        condition=dp.Condition(operator=Operator.LESS, value=0),
                    )
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
                    dp.FormattingRule(
                        style={"color": "red"},
                        condition=dp.Condition(operator=Operator.EQUAL, value=True),
                    )
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
            dp.Legend(
                items=[dp.LegendItem(icon="wb-icon-thumbs-up-full", label="Good Stuff")]
            ),
            dp.Legend(
                key="status_field",
                items=[
                    dp.LegendItem(
                        icon="wb-icon-thumbs-up-full", label="Status1", value="status1"
                    ),
                    dp.LegendItem(
                        icon="wb-icon-thumbs-up-full", label="Status2", value="status2"
                    ),
                    dp.LegendItem(
                        icon="wb-icon-thumbs-up-full", label="Status3", value="status3"
                    ),
                ],
            ),
        ],
        formatting=[
            dp.Formatting(
                column="integer_field",
                formatting_rules=[
                    dp.FormattingRule(
                        icon="wb-icon-thumbs-up-full", condition=("<", 5000)
                    ),
                    dp.FormattingRule(
                        style={"backgroundColor": "rgb(80,220,100)"},
                        condition=("<", 5000),
                    ),
                ],
            ),
        ],
    )

    INSTANCE_DISPLAY = dp.InstanceDisplay(
        sections=[
            dp.Section(
                fields=dp.FieldSet(
                    fields=[
                        dp.FieldSet(
                            fields=[
                                "image_field",
                                ["char_field", ["integer_field", "float_field"]],
                            ]
                        ),
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
            dp.Section(
                title="Related Models", section_list=dp.SectionList(key="related_model")
            ),
        ]
    )

    queryset = ModelTest.objects.all()
    serializer_class = ModelTestSerializer
    filterset_class = ModelTestFilterSet
    search_fields = ["char_field"]
    ordering_fields = ["char_field", "date_field", "float_field", "decimal_field"]

    def get_aggregates(self, queryset, **kwargs):
        return {
            "date_field": {
                "Latest Date": queryset.aggregate(ld=Max("date_field"))["ld"]
            },
            "integer_field": {
                "Σ": queryset.aggregate(s=Sum("integer_field"))["s"],
                "μ": queryset.aggregate(avg=Avg("integer_field"))["avg"],
            },
        }

    def get_queryset(self):
        return super().get_queryset().annotate(annotated_char_field=F("char_field"))

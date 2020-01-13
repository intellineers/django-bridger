from django.db.models import Avg, Max, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from bridger import buttons as bt
from bridger import display as dp
from bridger import viewsets

from .filters import ModelTestFilterSet
from .models import ModelTest, RelatedModelTest
from .serializers import (
    ModelTestRepresentationSerializer,
    ModelTestSerializer,
    RelatedModelTestSerializer,
)


class ModelTestRepresentationViewSet(viewsets.RepresentationModelViewSet):
    queryset = ModelTest.objects.all()
    serializer_class = ModelTestRepresentationSerializer


class ModelTestModelViewSet(viewsets.ModelViewSet):
    ENDPOINT = "modeltest-list"

    INSTANCE_WIDGET_TITLE = "{{char_field}}"
    LIST_WIDGET_TITLE = "List"
    CREATE_WIDGET_TITLE = "Create"

    LIST_DISPLAY = dp.ListDisplay(
        fields=[
            dp.Field(key="char_field", label="Char"),
            dp.Field(key="integer_field", label="Integer"),
            dp.Field(key="float_field", label="Float"),
            dp.Field(key="percent_field", label="Percent"),
            dp.Field(key="decimal_field", label="Decimal"),
            dp.Field(key="datetime_field", label="DateTime"),
            dp.Field(key="date_field", label="Date"),
            dp.Field(key="time_field", label="Time"),
            dp.Field(key="boolean_field", label="Boolean"),
            dp.Field(key="choice_field", label="Choice"),
            dp.Field(key="status_field", label="Status"),
            dp.Field(key="image_field", label="Image"),
            dp.Field(key="file_field", label="File"),
        ],
        legends=[dp.Legend(items=[dp.LegendItem(icon="wb-icon", label="something")])],
        formatting=[
            dp.RowFormatting(
                column="integer_field",
                conditions=[
                    dp.RowIconCondition(
                        icon="wb-icon-thumbs-up-full", condition=("<", 5000)
                    ),
                    dp.RowStyleCondition(
                        style={"backgroundColor": "rgb(100, 100, 100)"},
                        condition=("<", 5000),
                    ),
                ],
            )
        ],
    )

    INSTANCE_DISPLAY = dp.InstanceDisplay(
        sections=[
            dp.Section(
                fields=dp.FieldSet(
                    fields=[
                        "char_field",
                        "text_field",
                        "integer_field",
                        "float_field",
                        "percent_field",
                        "decimal_field",
                        "datetime_field",
                        "date_field",
                        "time_field",
                        "boolean_field",
                        "choice_field",
                        "status_field",
                        "image_field",
                        "file_field",
                    ]
                )
            )
        ]
    )

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    queryset = ModelTest.objects.all()
    serializer_class = ModelTestSerializer
    filter_class = ModelTestFilterSet

    search_fields = ("char_field",)
    ordering_fields = ("char_field", "date_field", "float_field", "decimal_field")

    def get_aggregates(self, queryset, paginated_queryset):
        return {
            "date_field": {
                "Latest Date": queryset.aggregate(ld=Max("date_field"))["ld"]
            },
            "integer_field": {
                "Σ": queryset.aggregate(s=Sum("integer_field"))["s"],
                "μ": queryset.aggregate(avg=Avg("integer_field"))["avg"],
            },
        }

    def get_messages(self, request, queryset=None, paginated_queryset=None):
        return {"message": "ABC1"}


class RelatedModelTestModelViewSet(viewsets.ModelViewSet):
    ENDPOINT = "relatedmodeltest-list"
    LIST_DISPLAY = dp.ListDisplay(
        fields=[
            dp.Field(key="char_field", label="Char"),
            dp.Field(key="model_test", label="Model"),
        ]
    )
    INSTANCE_DISPLAY = dp.InstanceDisplay(
        sections=[dp.Section(fields=dp.FieldSet(fields=["char_field", "model_test"]))]
    )

    queryset = RelatedModelTest.objects.all()
    serializer_class = RelatedModelTestSerializer

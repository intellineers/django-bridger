from django.db.models import Max

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
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
    INSTANCE_WIDGET_TITLE = "Instance"
    LIST_WIDGET_TITLE = "List"
    CREATE_WIDGET_TITLE = "Create"
    LIST_DISPLAY = dp.ListDisplay(
        fields=[
            dp.Field(key="char_field", label="Char"),
            dp.Field(key="datetime_field", label="DateTime"),
            dp.Field(key="date_field", label="Date"),
            dp.Field(key="time_field", label="Time"),
        ],
        legends=[dp.Legend(items=[dp.LegendItem(icon="wb-icon", label="something")])],
    )
    INSTANCE_DISPLAY = dp.InstanceDisplay(
        sections=[
            dp.Section(
                fields=dp.FieldSet(
                    fields=["char_field", "datetime_field", "date_field", "time_field"]
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

    def get_aggregates(self, queryset, paginated_queryset):
        return {
            "date_field": {
                "Latest Date": queryset.aggregate(ld=Max("date_field"))["ld"]
            }
        }


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

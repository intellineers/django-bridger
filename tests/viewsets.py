from django.db.models import Max

from bridger import display as dp
from bridger import viewsets

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
    LIST_DISPLAY = dp.ListDisplay(
        fields=[
            dp.Field(key="char_field", label="Char"),
            dp.Field(key="datetime_field", label="DateTime"),
            dp.Field(key="date_field", label="Date"),
            dp.Field(key="time_field", label="Time"),
        ]
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

    queryset = ModelTest.objects.all()
    serializer_class = ModelTestSerializer

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

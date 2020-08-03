from django.db.models import Avg, F, Max, Sum
from django.utils import timezone

from bridger import buttons as bt
from bridger import display as dp
from bridger.enums import Operator, Unit
from bridger.messages import info
from bridger.serializers import DateTimeField, ListSerializer
from bridger.viewsets import ModelViewSet, RepresentationModelViewSet
from tests.filters import ModelTestFilterSet
from tests.models import ModelTest
from tests.serializers import ModelTestRepresentationSerializer, ModelTestSerializer

from .display import ModelTestDisplayConfig
from .titles import ModelTestTitleConfig
from .preview import ModelTestPreviewConfig

class ModelTestRepresentationViewSet(RepresentationModelViewSet):
    queryset = ModelTest.objects.all()
    serializer_class = ModelTestRepresentationSerializer

    search_fields = ["char_field"]


class ModelTestModelViewSet(ModelViewSet):
    # LIST_DOCS = "tests/endpoint_documentation/model_test.md"
    # INSTANCE_DOCS = "# Instance Doc\n"

    display_config_class = ModelTestDisplayConfig
    title_config_class = ModelTestTitleConfig
    preview_config_class = ModelTestPreviewConfig

    queryset = ModelTest.objects.all()
    serializer_class = ModelTestSerializer
    filterset_class = ModelTestFilterSet
    search_fields = ["char_field"]
    ordering_fields = ["char_field", "date_field", "float_field", "decimal_field"]

    def get_aggregates(self, queryset, **kwargs):
        return {
            "date_field": {"Latest Date": queryset.aggregate(ld=Max("date_field"))["ld"]},
            "integer_field": {
                "Σ": queryset.aggregate(s=Sum("integer_field"))["s"],
                "μ": queryset.aggregate(avg=Avg("integer_field"))["avg"],
            },
        }

    def get_queryset(self):
        return super().get_queryset().annotate(annotated_char_field=F("char_field"))

    def get_serializer_changes(self, serializer):
        if not isinstance(serializer, ListSerializer) and hasattr(serializer, "fields"):
            serializer.fields["datetime_field"] = DateTimeField(label="Datetime", default=timezone.now())
        return serializer

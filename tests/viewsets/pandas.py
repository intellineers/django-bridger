from django.db.models import F

from bridger import display as dp
from bridger.pandas.views import PandasAPIView
from bridger.pandas import fields as pf
from bridger.serializers import decorator

from tests.filters import PandasFilterSet
from tests.models import ModelTest


class MyPandasView(PandasAPIView):

    search_fields = ["char_field"]
    filterset_class = PandasFilterSet

    INSTANCE_ENDPOINT = "modeltest-list"
    LIST_ENDPOINT = "pandas_view"
    LIST_TITLE = "Pandas List"

    LIST_DISPLAY = dp.ListDisplay(
        fields=[
            dp.Field(key="char_field", label="Char"),
            dp.Field(key="integer_field", label="Integer"),
            dp.Field(key="integer_annotated", label="Integer Anno"),
        ],
    )

    def get_filterset_class(self, request):
        return PandasFilterSet

    pandas_fields = pf.PandasFields(
        fields=[
            pf.PKField(key="id", label="ID"),
            pf.CharField(key="char_field", label="Char"),
            pf.FloatField(
                key="integer_field",
                label="Integer",
                precision=2,
                percent=True,
                decorators=[decorator(position="left", value="@")],
            ),
            pf.FloatField(
                key="integer_annotated", label="Integer Annotated", precision=2,
            ),
        ]
    )
    queryset = ModelTest.objects.all()
    ordering_fields = ["integer_field", "integer_annotated"]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(integer_annotated=F("integer_field") - 1)
        return qs

    def get_aggregates(self, request, df):
        return {
            "integer_field": {
                "Σ": df["integer_field"].sum(),
                "μ": df["integer_field"].mean(),
            }
        }

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
        ],
    )

    pandas_fields = pf.PandasFields(
        fields=[
            pf.PKField(key="id", label="ID"),
            pf.CharField(key="char_field", label="Char"),
            pf.FloatField(
                key="integer_field",
                label="Integer",
                precision=2,
                decorators=[decorator(position="left", value="@")],
            ),
        ]
    )
    queryset = ModelTest.objects.all()
    ordering_fields = ["integer_field"]

    def get_aggregates(self, request, df):
        return {
            "integer_field": {
                "Σ": df["integer_field"].sum(),
                "μ": df["integer_field"].mean(),
            }
        }

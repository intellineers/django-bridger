import logging
from collections import defaultdict

import pandas as pd
import plotly.graph_objects as go
from django.db.models import Avg, Max, Sum
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, views
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.serializers import ListSerializer

from bridger import buttons as bt
from bridger import display as dp
from bridger import viewsets
from bridger.enums import Unit
from bridger.filters import DjangoFilterBackend
from bridger.pandas import fields as pf
from bridger.pandas.views import PandasAPIView
from bridger.serializers import PrimaryKeyRelatedField

from .filters import CalendarFilter, ModelTestFilterSet, PandasFilterSet, RelatedModelTestFilterSet
from .models import ModelTest, RelatedModelTest
from .serializers import (
    CalendarModelTestSerializer,
    ModelTestRepresentationSerializer,
    ModelTestSerializer,
    RelatedModelTestRepresentationSerializer,
    RelatedModelTestSerializer
)

logger = logging.getLogger(__name__)


class MyPandasView(PandasAPIView):

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["char_field"]
    filter_class = PandasFilterSet

    INSTANCE_ENDPOINT = "modeltest-list"
    LIST_ENDPOINT = "pandas_view"
    LIST_WIDGET_TITLE = "Pandas List"

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
            pf.FloatField(key="integer_field", label="Integer", precision=2),
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


class ModelTestChartViewSet(viewsets.ChartViewSet):

    IDENTIFIER = "tests:chart"
    queryset = ModelTest.objects.all()

    def get_plotly(self, queryset):
        df = pd.DataFrame(
            queryset.order_by("date_field").values("date_field", "integer_field")
        )
        fig = go.Figure(
            [
                go.Scatter(
                    x=df.date_field,
                    y=df.integer_field,  # fill='tozeroy',
                    line=dict(width=1),
                    # line=dict(color=f"rgb({red}, {green}, {blue})", width=1),
                    # fillcolor=f"rgba({red}, {green}, {blue}, 0.1)"
                )
            ]
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(
                title="",
                titlefont=dict(color="#000000"),
                tickfont=dict(color="#000000"),
                anchor="x",
                side="right",
                showline=True,
                linewidth=1,
                linecolor="black",
            ),
            yaxis_type="log",
            xaxis=dict(
                title="",
                titlefont=dict(color="#000000"),
                tickfont=dict(color="#000000"),
                showline=True,
                linewidth=0.5,
                linecolor="black",
                showgrid=True,
                gridcolor="lightgray",
                gridwidth=1,
            ),
            autosize=True,
            xaxis_rangeslider_visible=True,
        )
        return fig


class ModelTestRepresentationViewSet(viewsets.RepresentationModelViewSet):
    queryset = ModelTest.objects.all()
    serializer_class = ModelTestRepresentationSerializer

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

    search_fields = ["char_field"]


class ModelTestModelViewSet(viewsets.ModelViewSet):
    ENDPOINT = "modeltest-list"

    INSTANCE_WIDGET_TITLE = "{{char_field}}"
    LIST_WIDGET_TITLE = "List"
    CREATE_WIDGET_TITLE = "Create"

    PREVIEW_BUTTONS = [bt.HyperlinkButton(key="hl-bt", icon="wb-icon-trash")]
    PREVIEW_DISPLAY = """<p>Char: {{char_field}}</p>"""

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
            dp.Field(key="related_models", label="Related"),
            dp.Field(key="file_field", label="File"),
        ],
        legends=[
            dp.Legend(
                items=[dp.LegendItem(icon="wb-icon-thumbs-up-full", label="Good Stuff")]
            )
        ],
        formatting=[
            dp.RowFormatting(
                column="integer_field",
                conditions=[
                    dp.RowIconCondition(
                        icon="wb-icon-thumbs-up-full", condition=("<", 5000)
                    ),
                    dp.RowStyleCondition(
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
                        "char_field",
                        "text_field",
                        "integer_field",
                        "float_field",
                        "percent_field",
                        "decimal_field",
                        "datetime_field",
                        "datetime_field1",
                        "date_field",
                        "time_field",
                        "boolean_field",
                        "choice_field",
                        "status_field",
                        "image_field",
                        "file_field",
                    ]
                )
            ),
            dp.Section(section_list=dp.SectionList(key="related_model")),
        ]
    )

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    queryset = ModelTest.objects.all()
    serializer_class = ModelTestSerializer
    # filter_class = ModelTestFilterSet
    filterset_fields = {
        "integer_field": ["lte", "gte", "exact"],
        "char_field": ["exact", "icontains"],
        "datetime_field": ["lte", "gte"],
        "status_field": ["exact"],
    }

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

    def get_messages(
        self, request, queryset=None, paginated_queryset=None, instance=None
    ):
        return [{"message": "ABC1", "type": "INFO"}]


class ModelTestModelCalendarViewSet(
    ModelTestModelViewSet, viewsets.InfiniteDataModelView
):

    filterset_class = CalendarFilter
    serializer_class = CalendarModelTestSerializer

    LIST_ENDPOINT = "calendar-list"
    INSTANCE_ENDPOINT = DELETE_ENDPOINT = CREATE_ENDPOINT = "modeltest-list"

    LIST_DISPLAY = dp.ListDisplay(
        fields=[
            dp.Field(key="char_field", label="Char",),
            dp.Field(key="datetime_field", label="DateTime",),
            dp.Field(key="datetime_field1", label="DateTime",),
        ],
        calendar=dp.Calender(
            title="char_field",
            start="datetime_field",
            end="datetime_field1",
            filter_date_gte="start",
            filter_date_lte="end",
        ),
    )


class RelatedModelTestRepresentationViewSet(viewsets.RepresentationModelViewSet):
    queryset = RelatedModelTest.objects.all()
    serializer_class = RelatedModelTestRepresentationSerializer


class RelatedModelTestModelViewSet(viewsets.ModelViewSet):
    ENDPOINT = "relatedmodeltest-list"
    LIST_DISPLAY = dp.ListDisplay(
        fields=[
            dp.Field(key="char_field", label="Char", col=Unit.FRACTION(2)),
            dp.Field(key="model_test", label="Model", col=Unit.FRACTION(2)),
            dp.Field(key="_left", col=Unit.REM(2)),
            dp.Field(key="_right", col=Unit.REM(2)),
        ]
    )
    INSTANCE_DISPLAY = dp.InstanceDisplay(
        sections=[
            dp.Section(
                fields=dp.FieldSet(fields=["char_field", "model_test", "model_tests"])
            )
        ]
    )

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filter_fields = {"model_test": ["exact"], "char_field": ["exact"]}
    search_fields = ["char_field"]

    queryset = RelatedModelTest.objects.all()
    serializer_class = RelatedModelTestSerializer

    def get_serializer_changes(self, serializer):
        if not isinstance(serializer, ListSerializer):
            default_values = ModelTest.objects.all()[:3].values_list("id", flat=True)
            serializer.fields["model_tests"].child_relation.default = default_values

        return serializer

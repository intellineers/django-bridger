import pandas as pd
from plotly import graph_objects as go

from bridger.viewsets import ChartViewSet
from tests.models import ModelTest


class ModelTestChartViewSet(ChartViewSet):

    IDENTIFIER = "tests:chart"
    queryset = ModelTest.objects.all()

    filterset_fields = {"date_field": ["lte", "gte"]}
    ordering_fields = ("date_field",)


    def get_plotly(self, queryset):
        df = pd.DataFrame(queryset.order_by("date_field").values("date_field", "integer_field"))
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

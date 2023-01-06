import random
from typing import Optional

import plotly.express as px
import plotly.graph_objs as go

from wildcoeus.dashboards.component.chart import ChartSerializer


class ScatterChartSerializer(ChartSerializer):
    x: Optional[str] = None
    y: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    mode: Optional[str] = "markers"

    def get_x(self, df) -> str:
        return self.x

    def get_y(self, df) -> str:
        return self.y

    def get_size(self, df) -> str:
        return self.size

    def to_fig(self, df) -> go.Figure:
        fig = px.scatter(
            df,
            x=self.get_x(df),
            y=self.get_y(df),
            size=self.get_size(df),
            color=self.color,
        )
        fig = fig.update_traces(mode=self.mode)

        return fig


class BarChartSerializer(ChartSerializer):
    x: Optional[str] = None
    y: Optional[str] = None
    color: Optional[str] = None
    barmode: Optional[str] = "group"

    def get_x(self, df) -> str:
        return self.x

    def get_y(self, df) -> str:
        return self.y

    def to_fig(self, df) -> go.Figure:
        fig = px.histogram(
            df,
            x=self.get_x(df),
            y=self.get_y(df),
            color=self.color,
            barmode=self.barmode,
            text_auto=True,
        )

        return fig


class ExampleChartSerializer(BarChartSerializer):
    x = "nation"
    y = "count"
    layout = dict(
        xaxis_title="Nation",
        yaxis_title="Total Medals",
        font=dict(family="Courier New, monospace", size=14, color="RebeccaPurple"),
    )

    class Meta:
        title = "Total Medals"

    def get_data(self, *args, **kwargs):
        df = px.data.medals_long()
        filters = kwargs.get("filters") or {}
        if "medal" in filters and filters["medal"] != "all":
            medal = filters["medal"]
            return df.query(f"medal == '{medal}'")

        return df


class ExampleStackedChartSerializer(BarChartSerializer):
    x = "nation"
    y = "count"
    color = "medal"

    class Meta:
        title = "Medals Split"

    def get_data(self, *args, **kwargs):
        df = px.data.medals_long()
        filters = kwargs.get("filters") or {}
        if "medal" in filters and filters["medal"] != "all":
            medal = filters["medal"]
            return df.query(f"medal == '{medal}'")

        return df


class ExampleBubbleChartSerializer(ScatterChartSerializer):
    x = "sepal_width"
    y = "sepal_length"
    color = "species"
    size = "petal_length"

    class Meta:
        title = "Bubble Chart Example"

    def get_data(self, *args, **kwargs):
        return px.data.iris()


class ExampleGaugeChartSerializer(ChartSerializer):
    class Meta:
        title = "Gauge Speed Example"

    def get_data(self, *args, **kwargs):
        return random.randint(200, 500)

    def to_fig(self, data) -> go.Figure:
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number", value=data, domain={"x": [0, 1], "y": [0, 1]}
            )
        )

        return fig

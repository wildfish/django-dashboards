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

    @classmethod
    def get_x(cls, df) -> str:
        return cls.x

    @classmethod
    def get_y(cls, df) -> str:
        return cls.y

    @classmethod
    def get_size(cls, df) -> str:
        return cls.size

    @classmethod
    def to_fig(cls, df) -> go.Figure:
        fig = px.scatter(
            df,
            x=cls.get_x(df),
            y=cls.get_y(df),
            size=cls.get_size(df),
            color=cls.color,
        )
        fig = fig.update_traces(mode=cls.mode)

        return fig


class BarChartSerializer(ChartSerializer):
    x: Optional[str] = None
    y: Optional[str] = None
    color: Optional[str] = None
    barmode: Optional[str] = "group"

    @classmethod
    def get_x(cls, df) -> str:
        return cls.x

    @classmethod
    def get_y(cls, df) -> str:
        return cls.y

    @classmethod
    def to_fig(cls, df) -> go.Figure:
        fig = px.histogram(
            df,
            x=cls.get_x(df),
            y=cls.get_y(df),
            color=cls.color,
            barmode=cls.barmode,
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
        title = "Medals"

    @classmethod
    def get_data(cls, *args, **kwargs):
        df = px.data.medals_long()
        filters = kwargs.get("filters") or {}
        if "animal" in filters and filters["animal"] in df:
            animal = filters["animal"]
            df = {animal: df[animal]}

        return df


class ExampleStackedChartSerializer(BarChartSerializer):
    x = "nation"
    y = "count"
    color = "medal"

    class Meta:
        title = "Medals Stacked"

    @classmethod
    def get_data(cls, *args, **kwargs):
        df = px.data.medals_long()
        filters = kwargs.get("filters") or {}
        if "animal" in filters and filters["animal"] in df:
            animal = filters["animal"]
            df = {animal: df[animal]}

        return df


class ExampleBubbleChartSerializer(ScatterChartSerializer):
    x = "sepal_width"
    y = "sepal_length"
    color = "species"
    size = "petal_length"

    class Meta:
        title = "Bubble Chart Example"

    @classmethod
    def get_data(cls, *args, **kwargs):
        return px.data.iris()


class ExampleGaugeChartSerializer(ChartSerializer):
    class Meta:
        title = "Gauge Speed Example"

    @classmethod
    def get_data(cls, *args, **kwargs):
        return random.randint(200, 500)

    @classmethod
    def to_fig(cls, data) -> go.Figure:
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number", value=data, domain={"x": [0, 1], "y": [0, 1]}
            )
        )

        return fig

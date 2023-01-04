import plotly.express as px

from wildcoeus.dashboards.component.chart import ScatterChartSerializer, HistogramChartSerializer


class ExampleChartSerializer(HistogramChartSerializer):
    class Meta:
        x = "nation"
        y = "count"
        title = "Medals"

    @classmethod
    def get_data(cls, *args, **kwargs):
        df = px.data.medals_long()
        filters = kwargs.get("filters") or {}
        if "animal" in filters and filters["animal"] in df:
            animal = filters["animal"]
            df = {animal: df[animal]}

        return df


class ExampleStackedChartSerializer(HistogramChartSerializer):
    class Meta:
        x = "nation"
        y = "count"
        color = "medal"
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
    class Meta:
        x = "nation"
        y = "count"
        color = "medal"
        title = "Bubble Chart Example"
        mode = "markers"

    @classmethod
    def get_data(cls, *args, **kwargs):
        df = px.data.medals_long()
        return df

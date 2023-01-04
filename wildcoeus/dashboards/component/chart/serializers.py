import json

from typing import Any, Dict, List, Optional

from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet

import pandas as pd
import plotly.express as px


class PlotyExpressHelper:
    @staticmethod
    def empty_chart(title):
        return json.dumps(
            {
                "layout": {
                    "xaxis": {"visible": False},
                    "yaxis": {"visible": False},
                    "annotations": [
                        {
                            "text": f"{title} - No data",
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                            "font": {"size": 28},
                        }
                    ],
                }
            }
        )

    @staticmethod
    def _all(fig):
        fig.update_layout(template="seaborn")
        return fig

    @classmethod
    def chart_layout(
        cls, fig, slider: bool = False, layout: Optional[Dict[str, Any]] = None
    ):
        fig = cls._all(fig)
        fig.update_xaxes(rangeslider_visible=slider)

        if layout:
            fig.update_layout(**layout)

        return fig.update_layout()


class ChartSerializerType(type):
    def __new__(mcs, name, bases, attrs):
        chart_serializer_class = super().__new__(mcs, name, bases, attrs)
        attr_meta = attrs.get("Meta", None)
        meta = attr_meta or getattr(chart_serializer_class, "Meta", None)
        base_meta = getattr(chart_serializer_class, "_meta", None)
        chart_serializer_class._meta = meta

        if base_meta:
            if not hasattr(meta, "title"):
                chart_serializer_class._meta.title = base_meta.title
            if not hasattr(meta, "queryset"):
                chart_serializer_class._meta.queryset = base_meta.queryset
            if not hasattr(meta, "model"):
                chart_serializer_class._meta.model = base_meta.model
            if not hasattr(meta, "layout"):
                chart_serializer_class._meta.layout = base_meta.layout
            if not hasattr(meta, "color"):
                chart_serializer_class._meta.color = base_meta.color
            if not hasattr(meta, "orientation"):
                chart_serializer_class._meta.orientation = base_meta.orientation
            if not hasattr(meta, "barmode"):
                chart_serializer_class._meta.barmode = base_meta.barmode
            if not hasattr(meta, "mode"):
                chart_serializer_class._meta.mode = base_meta.mode
            if not hasattr(meta, "width"):
                chart_serializer_class._meta.width = base_meta.width
            if not hasattr(meta, "height"):
                chart_serializer_class._meta.height = base_meta.height

        return chart_serializer_class


class ChartSerializer(metaclass=ChartSerializerType):
    class Meta:
        fields: List[str]
        title: Optional[str] = None
        model: Optional[str] = None
        queryset: Optional[str] = None
        layout: Optional[Dict[str, Any]] = None
        mode: Optional[str] = None
        color: Optional[str] = None
        orientation: Optional[str] = None
        barmode: Optional[str] = None
        width: Optional[int] = None
        height: Optional[int] = None

    @classmethod
    def serialize(cls, **serialize_kwargs) -> str:
        def _serialize(**kwargs) -> str:
            df = cls.get_data(**serialize_kwargs, **kwargs)
            fig = cls.to_fig(df)
            fig = PlotyExpressHelper.chart_layout(fig, layout=cls.Meta.layout)

            return fig.to_json()

        return _serialize

    @classmethod
    def get_fields(cls):
        return cls.Meta.fields

    @classmethod
    def get_data(cls, *args, **kwargs):
        queryset = cls.get_queryset(*args, **kwargs)
        queryset = queryset.values(*cls.get_fields())
        df = pd.DataFrame(queryset.iterator(), columns=cls.get_fields())

        return df

    @classmethod
    def get_queryset(cls, *args, **kwargs):
        """
        Return the list of items for this pipeline to run against.
        """
        if getattr(cls.Meta, "queryset", None) is not None:
            queryset = cls.Meta.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif cls.Meta.model is not None:
            queryset = cls.Meta.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {"cls": cls.__class__.__name__}
            )

        return queryset

    @classmethod
    def to_fig(cls, df) -> str:
        raise ImproperlyConfigured("ChartSerializer must have to_fig defined")


class ScatterChartSerializer(ChartSerializer):
    class Meta:
        x: Optional[str] = None
        y: Optional[str] = None
        color: Optional[str] = None
        mode: Optional[str] = "lines+markers"

    @classmethod
    def get_x(cls, df) -> str:
        return cls.Meta.x

    @classmethod
    def get_y(cls, df) -> str:
        return cls.Meta.y

    @classmethod
    def to_fig(cls, df) -> str:
        fig = px.scatter(
            df,
            x=cls.get_x(df),
            y=cls.get_y(df),
            color=cls.Meta.color,
            title=cls.Meta.title,
            width=cls.Meta.width,
            height=cls.Meta.height,
        )
        fig = fig.update_traces(mode=cls.Meta.mode)

        return fig


class BarChartSerializer(ChartSerializer):
    class Meta:
        x: Optional[str] = None
        y: Optional[str] = None
        color: Optional[str] = None
        orientation: Optional[str] = "v"

    @classmethod
    def get_x(cls, df) -> str:
        return cls.Meta.x

    @classmethod
    def get_y(cls, df) -> str:
        return cls.Meta.y

    @classmethod
    def to_fig(cls, df) -> str:
        fig = px.bar(
            df,
            x=cls.get_x(df),
            y=cls.get_y(df),
            color=cls.Meta.color,
            orientation=cls.Meta.orientation,
            title=cls.Meta.title,
            width=cls.Meta.width,
            height=cls.Meta.height,
        )

        return fig


class HistogramChartSerializer(ChartSerializer):
    class Meta:
        x: Optional[str] = None
        y: Optional[str] = None
        color: Optional[str] = None
        barmode: Optional[str] = 'group'

    @classmethod
    def get_x(cls, df) -> str:
        return cls.Meta.x

    @classmethod
    def get_y(cls, df) -> str:
        return cls.Meta.y

    @classmethod
    def to_fig(cls, df) -> str:
        fig = px.histogram(
            df,
            x=cls.get_x(df),
            y=cls.get_y(df),
            color=cls.Meta.color,
            barmode=cls.Meta.barmode,
            text_auto=True,
            title=cls.Meta.title,
            width=cls.Meta.width,
            height=cls.Meta.height,
        )

        return fig

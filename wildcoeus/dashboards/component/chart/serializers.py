from typing import Any, Callable, Dict, List, Optional

from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet

import pandas as pd
import plotly.graph_objs as go


class ChartSerializerType(type):
    def __new__(mcs, name, bases, attrs):
        chart_serializer_class = super().__new__(mcs, name, bases, attrs)
        attr_meta = attrs.get("Meta", None)
        meta = attr_meta or getattr(chart_serializer_class, "Meta", None)
        base_meta = getattr(chart_serializer_class, "_meta", None)
        chart_serializer_class._meta = meta

        if base_meta:
            if not hasattr(meta, "fields"):
                chart_serializer_class._meta.fields = base_meta.fields
            if not hasattr(meta, "queryset"):
                chart_serializer_class._meta.queryset = base_meta.queryset
            if not hasattr(meta, "model"):
                chart_serializer_class._meta.model = base_meta.model
            if not hasattr(meta, "title"):
                chart_serializer_class._meta.title = base_meta.title
            if not hasattr(meta, "width"):
                chart_serializer_class._meta.width = base_meta.width
            if not hasattr(meta, "height"):
                chart_serializer_class._meta.height = base_meta.height

        return chart_serializer_class


class ChartSerializer(metaclass=ChartSerializerType):
    meta_layout_attrs = ["title", "width", "height"]
    layout: Optional[Dict[str, Any]] = None

    class Meta:
        fields: Optional[List[str]] = None
        model: Optional[str] = None
        queryset: Optional[str] = None
        title: Optional[str] = None
        width: Optional[int] = None
        height: Optional[int] = None

    @classmethod
    def serialize(cls, **serialize_kwargs) -> Callable:
        def _serialize(**kwargs) -> str:
            df = cls.get_data(**serialize_kwargs, **kwargs)
            fig = cls.to_fig(df)
            fig = cls.apply_layout(fig)
            return fig.to_json()

        return _serialize

    @classmethod
    def get_fields(cls) -> Optional[List[str]]:
        return cls.Meta.fields

    @classmethod
    def apply_layout(cls, fig: go.Figure):
        layout = cls.layout or {}

        for attr in cls.meta_layout_attrs:
            layout.setdefault(attr, getattr(cls.Meta, attr))

        return fig.update_layout(**layout)

    @classmethod
    def convert_to_df(cls, data: Any, columns: List = None) -> pd.DataFrame:
        df = pd.DataFrame(data, columns=columns)
        return df

    @classmethod
    def get_data(cls, *args, **kwargs) -> pd.DataFrame:
        fields = cls.get_fields()
        queryset = cls.get_queryset(*args, **kwargs)
        if fields:
            queryset = queryset.values(*fields)
        df = cls.convert_to_df(queryset.iterator(), fields)

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
    def to_fig(cls, data: Any) -> go.Figure:
        raise NotImplementedError

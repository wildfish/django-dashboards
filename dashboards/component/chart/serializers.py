import json
from typing import Any, Dict, List, Optional

from django.core.exceptions import ImproperlyConfigured

import pandas as pd
import plotly.graph_objs as go

from dashboards.meta import ClassWithMeta


class ChartSerializer(ClassWithMeta):
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
    def preprocess_meta(cls, current_class_meta):
        title = getattr(current_class_meta, "title", None)

        if title and not hasattr(current_class_meta, "name"):
            current_class_meta.name = title

        if title and not hasattr(current_class_meta, "verbose_name"):
            current_class_meta.verbose_name = title

        return current_class_meta

    @classmethod
    def postprocess_meta(cls, current_class_meta, resolved_meta_class):
        if not hasattr(resolved_meta_class, "title"):
            resolved_meta_class.title = resolved_meta_class.verbose_name

        return resolved_meta_class

    def empty_chart(self):
        return json.dumps(
            {
                "layout": {
                    "xaxis": {"visible": False},
                    "yaxis": {"visible": False},
                    "annotations": [
                        {
                            "text": f"{self._meta.verbose_name} - No data",
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                            "font": {"size": 28},
                        }
                    ],
                }
            }
        )

    @classmethod
    def serialize(cls, **kwargs) -> str:
        self = cls()
        df = self.get_data(**kwargs)

        if isinstance(df, pd.DataFrame) and df.empty:
            return self.empty_chart()

        fig = self.to_fig(df)
        fig = self.apply_layout(fig)
        return fig.to_json()

    def get_fields(self) -> Optional[List[str]]:
        # TODO: for some reason mypy complains about this one line
        return self._meta.fields  # type: ignore

    def apply_layout(self, fig: go.Figure):
        layout = self.layout or {}

        for attr in self.meta_layout_attrs:
            layout.setdefault(attr, getattr(self._meta, attr))

        return fig.update_layout(**layout)

    def convert_to_df(self, data: Any, columns: Optional[List] = None) -> pd.DataFrame:
        return pd.DataFrame(data, columns=columns)

    def get_data(self, *args, **kwargs) -> pd.DataFrame:
        fields = self.get_fields()
        queryset = self.get_queryset(*args, **kwargs)
        if fields:
            queryset = queryset.values(*fields)

        try:
            df = self.convert_to_df(queryset.iterator(), fields)
        except KeyError:
            return pd.DataFrame()
        return df

    def get_queryset(self, *args, **kwargs):
        if self._meta.model is not None:
            queryset = self._meta.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(self)s is missing a QuerySet. Define "
                "%(self)s.model or override "
                "%(self)s.get_queryset()." % {"self": self.__class__.__name__}
            )

        return queryset

    def to_fig(self, data: Any) -> go.Figure:
        raise NotImplementedError

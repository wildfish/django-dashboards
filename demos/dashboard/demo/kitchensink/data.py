# data.py

import json
from datetime import timedelta

from django.contrib.auth.models import User
from django.db.models import Count

from demo.kitchensink.models import FlatText

from dashboards.component.stat import StatDateChangeSerializer
from dashboards.component.filters import GenericFilter
from .forms import ExampleForm, MedalForm

class DashboardData:
    def _apply_filter_age_range(self):
        pass

    @staticmethod
    def fetch_html(*args, **kwargs) -> str:
        return getattr(FlatText.objects.all().first(), "text", "Flat Text")

    @staticmethod
    def fetch_scatter_map_data(*args, **kwargs) -> str:
        return json.dumps(
            dict(
                data=[
                    dict(
                        lat=[40.7127, 51.5072],
                        lon=[-74.0059, 0.1275],
                        mode="lines",
                        type="scattergeo",
                        line={"width": 2, "color": "blue"},
                    )
                ],
                layout=dict(
                    title="London to NYC Great Circle",
                    showlegend=False,
                    geo={
                        "resolution": 50,
                        "showland": True,
                        "showlakes": True,
                        "landcolor": "rgb(204, 204, 204)",
                        "countrycolor": "rgb(204, 204, 204)",
                        "lakecolor": "rgb(255, 255, 255)",
                        "projection": {"type": "equirectangular"},
                        "coastlinewidth": 2,
                        "lataxis": {
                            "range": [20, 60],
                            "showgrid": True,
                            "tickmode": "linear",
                            "dtick": 10,
                        },
                        "lonaxis": {
                            "range": [-100, 20],
                            "showgrid": True,
                            "tickmode": "linear",
                            "dtick": 20,
                        },
                    },
                ),
            )
        )

    @staticmethod
    def fetch_sse_chart_data(*args, **kwargs) -> str:
        return json.dumps(
            dict(
                data=[
                    dict(
                        y=list([1, 2, 3]),
                        type="scatter",
                        mode="lines",
                    )
                ]
            )
        )

    @staticmethod
    def fetch_users_data(form):
        queryset = User.objects.all()

        # Apply filtering based on the GenericFilter
        if form.is_valid():
            user_filter = GenericFilter(data=form.cleaned_data, queryset=queryset)
            queryset = user_filter.qs

        # Apply additional filtering based on your requirements
        # For example, filtering by age_range if it's available in the form
        age_range = form.cleaned_data.get('age_range')
        if age_range:
            queryset = queryset.filter(age__range=age_range)

        # You can apply additional filtering based on your requirements
        # For example, filtering by country if it's available in the form
        country = form.cleaned_data.get('country')
        if country:
            queryset = queryset.filter(country=country)

        return queryset


class UsersThisWeek(StatDateChangeSerializer):
    class Meta:
        annotation_field = "id"
        annotation = Count
        model = User
        date_field_name = "date_joined"
        previous_delta = timedelta(days=7)
        title = "New Users"
        unit = " people"

from random import randint

from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Count

from datorum.component.chart import ChartData
from datorum.component.map import MapData
from datorum.component.table import (
    DatatablesQuerysetFilter,
    DatatablesQuerysetSort,
    ReactTablesQuerysetSort,
    TableData,
    TablePaging,
    ToTable,
)
from datorum.component.text import StatData

from demo.churn.models import Customer, Scenario
from demo.churn.utils import us_state_to_abbrev


class ChurnSummaryData:
    @staticmethod
    def fetch_forecast_analysis(*args, **kwargs) -> ChartData:
        """
        Build a for now arbitrary calculation against each scenario as a forecast of MGM.
        """
        current_mgm = Customer.objects.monthly_gross_margin()

        scenario_traces = []
        for scenario in Scenario.objects.all():
            forecast = randint(950, 1500) / 1000

            trace = ChartData.Trace(
                x=["Current MGM", "Forecast MGM"],
                y=[current_mgm, float(current_mgm) * forecast],
                mode=ChartData.Trace.Mode.LINE,
                name=scenario.name,
                type=ChartData.Trace.Type.SCATTER,
            )
            scenario_traces.append(trace)

        return ChartData(
            data=scenario_traces,
            layout={
                "title": "Forecast Analysis",
            })

    @staticmethod
    def fetch_monthly_gross_margin(*args, **kwargs) -> StatData:
        mgm = Customer.objects.monthly_gross_margin()
        return StatData(text=f"£{intcomma(mgm)}", sub_text="Monthly Gross Margin")

    @staticmethod
    def fetch_actual_churn_rate(*args, **kwargs) -> StatData:
        rate = Customer.objects.actual_churn_rate()
        return StatData(text=f"{rate}%", sub_text="Actual Churn Rate")

    @staticmethod
    def fetch_churn_risk_predictor(*args, **kwargs) -> ChartData:
        data = {"giraffes": 20, "orangutans": 14, "monkeys": 23}

        return ChartData(
            data=[
                ChartData.Trace(
                    x=list(data.keys()),
                    y=list(data.values()),
                    type=ChartData.Trace.Type.BAR,
                )
            ]
        )

    @staticmethod
    def fetch_churn_by_geography(*args, **kwargs) -> MapData:
        data = (
            Customer.objects.churned()
            .values("location")
            .annotate(churned=Count("pk"))
            .values("location", "churned")
        )

        locations = []
        locations_text = []
        churned = []

        for d in data:
            locations.append(us_state_to_abbrev[d["location"]])
            locations_text.append(d["location"])
            churned.append(d["churned"])

        return MapData(
            data=[
                MapData.Choropleth(
                    locationmode="USA-states",
                    locations=locations,
                    z=churned,
                    text=locations_text,
                    autocolorscale=True,
                )
            ],
            layout={
                "title": "Churn Risk By State",
                "geo": {
                    "scope": "usa",
                },
            },
        )

    @staticmethod
    def fetch_actual_churn_data(*args, **kwargs) -> TableData:
        # filtering, sorting
        filters = kwargs["filters"]
        # pagination
        start = int(filters.get("start", 0))
        length = int(filters.get("length", 10))

        # todo: can these be gotten from Table columns?
        fields = [
            "reference",
            "product_cloud",
            "product_connectivity",
            "product_licenses",
            "product_managed_services",
            "product_backup",
            "product_hardware",
            "recurring_revenue",
            "non_recurring_revenue",
        ]

        # todo: can this be done better i.e. if mpa do x if spa do y?
        if "draw" in filters:  # assume its datatables request (mpa) if draw in filters
            filter_class = DatatablesQuerysetFilter
            sort_class = DatatablesQuerysetSort
        else:
            filter_class = None  # no search in react tables
            sort_class = ReactTablesQuerysetSort

        table_data = ToTable(
            data=Customer.objects.churned(),
            filters=filters,
            count_func=lambda qs: qs.count(),
            fields=fields,
            filter_class=filter_class,
            sort_class=sort_class,
        ).get_data(start, length)

        return table_data

    @staticmethod
    def fetch_churn_table(*args, **kwargs) -> TableData:
        """
        Customer in the system.
        """
        # filtering, sorting
        filters = kwargs["filters"]
        # pagination
        start = int(filters.get("start", 0))
        length = int(filters.get("length", 10))

        # todo: can these be gotten from Table columns?
        fields = [
            "id",
            "reference",
            "phone",
            "email",
        ]

        # todo: can this be done better i.e. if mpa do x if spa do y?
        if "draw" in filters:  # assume its datatables request (mpa) if draw in filters
            filter_class = DatatablesQuerysetFilter
            sort_class = DatatablesQuerysetSort
        else:
            filter_class = None  # no search in react tables
            sort_class = ReactTablesQuerysetSort

        table_data = ToTable(
            data=Customer.objects.churned(),
            filters=filters,
            count_func=lambda qs: qs.count(),
            fields=fields,
            filter_class=filter_class,
            sort_class=sort_class,
        ).get_data(start, length)

        return table_data

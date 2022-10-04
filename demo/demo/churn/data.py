import math

from django.contrib.humanize.templatetags.humanize import intcomma

from django.db.models import Count

from datorum.component.chart import ChartData
from datorum.component.map import MapData
from datorum.component.table import TableData, TablePaging
from datorum.component.text import StatData
from datorum.utils import DatatablesQuerysetFilter, DatatablesQuerysetSort, ToTable, ReactTablesSort, \
    ReactTablesQuerysetSort

from demo.churn.models import Customer
from demo.churn.utils import us_state_to_abbrev


class ChurnSummaryData:
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
        data = Customer.objects.churned().values("location").annotate(churned=Count("pk")).values("location", "churned")

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
        filters = kwargs["filters"]
        # defaults
        draw = filters.get("draw", 0)
        start = int(filters.get("start", 0))
        length = int(filters.get("length", 25))

        field_to_name = {
            "reference": "reference",
            "product_cloud": "product_cloud",
            "product_connectivity": "product_connectivity",
            "product_licenses": "product_licenses",
        }

        # todo: can this be done better i.e. if mpa do x if spa do y?
        if "draw" in filters:  # assume its datatables request (mpa) if draw in filters
            filter_class = DatatablesQuerysetFilter
            sort_class = DatatablesQuerysetSort
        else:
            filter_class = None
            sort_class = ReactTablesQuerysetSort

        data = ToTable(
            data=Customer.objects.churned(),
            filters=filters,
            count_func=lambda x: x.count(),
            field_to_name=field_to_name,
            filter_class=filter_class,
            sort_class=sort_class,

        ).filter_data(start, length)

        paging = TablePaging(
            ssr=True,
            limit=length,
            page=data["page"],
            page_count=data["page_count"],
            total_items=data["recordsTotal"],
        )

        table_data = TableData(
            **data,
            draw=draw,
            paging=paging
        )

        return table_data

    @staticmethod
    def fetch_churn_table(*args, **kwargs) -> TableData:
        """
        Mock return some results for tabular.
        """
        request = kwargs["request"]
        field_to_name = {
            "id": "ID",
            "reference": "Reference",
            "phone": "Phone",
            "email": "Email",
        }
        data = ToTable(qs=Customer.objects.all(), request=request, field_to_name=field_to_name).filter_data(0, 25)

        table_data = TableData(
            data=data,
        )

        return table_data

from django.contrib.humanize.templatetags.humanize import intcomma

from datorum.component import Chart, Map, Stat, Table, Text
from datorum.component.layout import HTML, Card, ComponentLayout
from datorum.component.table import TableData, TablePaging
from datorum.component.text import StatData
from datorum.dashboard import Dashboard
from datorum.registry import registry

from demo.churn.data import ChurnSummaryData


class SummaryDashboard(Dashboard):
    number_risky_customers = Stat(
        value=StatData(text="2", sub_text="# Risky customers")
    )
    monthly_gross_margin = Stat(defer=ChurnSummaryData.fetch_monthly_gross_margin)
    actual_churn_rate = Stat(defer=ChurnSummaryData.fetch_actual_churn_rate)

    actual_churn_data = Table(
        defer=ChurnSummaryData.fetch_actual_churn_data,
        columns=[
            {"data": "reference", "title": "Reference"},
            {"data": "product_cloud", "title": "Product Cloud"},
            {"data": "product_connectivity", "title": "Product Connectivity"},
            {"data": "product_licenses", "title": "Product Licenses"},
        ],
        page_size=25,
    )
    churn_by_geography = Map(defer=ChurnSummaryData.fetch_churn_by_geography)

    # forecast_analysis = Chart(defer=ChurnSummaryData.fetch_churn_risk_predictor)
    # churn_factors = Chart(defer=ChurnSummaryData.fetch_churn_risk_predictor)
    #
    # churn_table = Table(defer=ChurnSummaryData.fetch_churn_table)
    table_test = Table(
        columns=[
            {"data": "id", "title": "ID"},
            {"data": "name", "title": "Name"},
            {"data": "progress", "title": "Progress"},
            {"data": "gender", "title": "Gender"},
            {"data": "dob", "title": "DOB"},
        ],
        page_size=10,
        value=TableData(
            data=[
                {
                    "id": 1,
                    "name": "Oli Bob",
                    "progress": 12,
                    "gender": "male",
                    "rating": 1,
                    "col": "red",
                    "dob": "19/02/1984",
                    "car": 1,
                },
                {
                    "id": 2,
                    "name": "Bob Oli",
                    "progress": 2,
                    "gender": "male",
                    "rating": 5,
                    "col": "blue",
                    "dob": "21/04/1995",
                    "car": 0,
                },
            ],
            paging=TablePaging(total_items=2, limit=10, page_count=2),
        ),
    )

    class Layout(Dashboard.Layout):
        components = ComponentLayout(
            HTML(
                "This is the Churn Summary Dashboard Demo",
                width=12,
            ),
            Card("table_test", width=12),
            # Card("number_risky_customers", width=4),
            # Card("monthly_gross_margin", width=4),
            # Card("actual_churn_rate", width=4),
            Card("actual_churn_data", width=12),
            # Card("churn_by_geography", width=4),
            # Card("forecast_analysis", width=6),
            # Card("churn_factors", width=6),
            # Card("churn_table", width=12),
        )

    class Meta:
        name = "Summary"


registry.register(SummaryDashboard)

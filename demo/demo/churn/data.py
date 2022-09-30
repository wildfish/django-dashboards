import csv

from django.contrib.humanize.templatetags.humanize import intcomma

import requests
from datorum.component.chart import ChartData
from datorum.component.map import MapData
from datorum.component.table import TableData, TablePaging
from datorum.component.text import StatData

from demo.churn.models import Customer


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
        url = "https://raw.githubusercontent.com/plotly/datasets/master/2014_usa_states.csv"
        r = requests.get(url)
        lines = [line.decode("utf-8") for line in r.iter_lines()]
        reader = csv.reader(lines, delimiter=",")
        locations = []
        z = []
        text = []
        for r in reader:
            locations.append(r[2])
            z.append(r[3])
            text.append(r[1])

        return MapData(
            data=[
                MapData.Choropleth(
                    locationmode="USA-states",
                    locations=locations[1:],
                    z=z[1:],
                    text=text[1:],
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
    def fetch_churn_table(*args, **kwargs) -> TableData:
        """
        Mock return some results for tabular.
        """
        data = [
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
                "name": "Mary May",
                "progress": 1,
                "gender": "female",
                "rating": 2,
                "col": "blue",
                "dob": "14/05/1982",
                "car": True,
            },
            {
                "id": 3,
                "name": "Christine Lobowski",
                "progress": 42,
                "gender": "female",
                "rating": 0,
                "col": "green",
                "dob": "22/05/1982",
                "car": "true",
            },
            {
                "id": 4,
                "name": "Brendon Philips",
                "progress": 100,
                "gender": "male",
                "rating": 1,
                "col": "orange",
                "dob": "01/08/1980",
            },
            {
                "id": 5,
                "name": "Margret Marmajuke",
                "progress": 16,
                "gender": "female",
                "rating": 5,
                "col": "yellow",
                "dob": "31/01/1999",
            },
            {
                "id": 6,
                "name": "Frank Harbours",
                "progress": 38,
                "gender": "male",
                "rating": 4,
                "col": "red",
                "dob": "12/05/1966",
                "car": 1,
            },
        ]

        table_data = TableData(
            headers=[
                "Id",
                "Name",
                "Progress",
                "Gender",
                "Rating",
                "Colour",
                "DOB",
                "Car",
            ],
            rows=data,
        )

        return table_data

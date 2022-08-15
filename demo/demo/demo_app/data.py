from demo.demo_app.models import FlatText


class DashboardData:
    def _apply_filter_age_range(self):
        pass

    @staticmethod
    def fetch_html(request):
        return FlatText.objects.all().first().text

    @staticmethod
    def fetch_gauge_chart_data(request):
        return [
            {
                "domain": {"x": [0, 1], "y": [0, 1]},
                "value": 2700,
                "title": {"text": "Average RPM"},
                "type": "indicator",
                "mode": "gauge+number",
            }
        ]

    @staticmethod
    def fetch_gauge_chart_data_two(request):
        return [
            {
                "domain": {"x": [0, 1], "y": [0, 1]},
                "value": 45,
                "title": {"text": "MPG"},
                "type": "indicator",
                "mode": "gauge+number+delta",
                "delta": {"reference": 38},
                "gauge": {
                    "axis": {"range": [None, 50]},
                    "steps": [
                        {"range": [0, 25], "color": "lightgray"},
                        {"range": [25, 40], "color": "gray"},
                    ],
                    "threshold": {
                        "line": {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value": 49,
                    },
                },
            }
        ]

    @staticmethod
    def fetch_bar_chart_data(request):
        return [
            {
                "x": ["giraffes", "orangutans", "monkeys"],
                "y": [20, 14, 23],
                "type": "bar",
            }
        ]

    @staticmethod
    def fetch_bubble_chart_data(request):
        return [
            {
                "x": [1, 2, 3, 4],
                "y": [10, 11, 12, 13],
                "mode": 'markers',
                "marker": {
                    "size": [40, 60, 80, 100]
                }
            }
        ]

    @staticmethod
    def fetch_table_data(request):
        """
        Mock return some results for tabular.
        """
        return [
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

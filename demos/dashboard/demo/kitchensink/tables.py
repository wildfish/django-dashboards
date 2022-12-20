from random import randrange

from wildcoeus.dashboards.component.table import TableSerializer


class ExampleTableSerializer(TableSerializer):
    class Meta:
        title = "Example table"
        columns = {
            "id": "Title",
            "name": "Name",
            "progress": "Progress",
            "gender": "Gender",
            "dob": "DOB",
        }

    @staticmethod
    def get_data(**kwargs):
        return [
            {
                "id": r,
                "name": f"Name {r}",
                "progress": randrange(100),
                "gender": "male",
                "rating": randrange(5),
                "col": "red",
                "dob": "19/02/1984",
                "car": randrange(10),
            }
            for r in range(10)
        ]

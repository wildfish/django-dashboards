from demo.vehicle.data import VehicleData

from dashboards.component.table import TableSerializer


class VehicleTableSerializer(TableSerializer):
    class Meta:
        title = "Vehicle table"
        columns = {
            "ref": "Reference",
            "type": "Type",
            "number_plate": "Number Plate",
            "current_mileage": "Mileage",
            "next_mot_due": "MOT Due",
        }

    def get_queryset(self, **kwargs):
        return VehicleData.get_queryset(filters=kwargs["filters"])

# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_dashboard_form__asdict 1"] = [
    {
        "choices": [],
        "field_type": "TextInput",
        "help_text": "",
        "id": "id_name",
        "label": "Name",
        "name": "name",
        "required": True,
        "value": "",
    },
    {
        "choices": [("one", "one"), ("two", "two"), ("three", "three")],
        "field_type": "Select",
        "help_text": "",
        "id": "id_number",
        "label": "Number",
        "name": "number",
        "required": True,
        "value": "",
    },
]

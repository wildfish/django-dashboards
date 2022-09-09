# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_view__component__deferred 1"] = {"isDeferred": True, "value": "value"}

snapshots["test_view__component__not_deferred 1"] = {
    "isDeferred": False,
    "value": "value",
}

snapshots["test_view__dashboard 1"] = {
    "Meta": {"name": "Test Dashboard", "slug": "test-dashboard"},
    "components": [
        {
            "isDeferred": False,
            "key": "component_1",
            "renderType": "Text",
            "value": "value",
            "width": 12,
        },
        {
            "isDeferred": True,
            "key": "component_2",
            "renderType": "Text",
            "value": None,
            "width": 12,
        },
    ],
}

snapshots["test_view__dashboard__not_found 1"] = None

snapshots["test_view__dashboards 1"] = [
    {
        "Meta": {"name": "Test Admin Dashboard", "slug": "test-admin-dashboard"},
        "components": [
            {
                "group": None,
                "groupWidth": None,
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "admin value",
                "width": 12,
            }
        ],
    },
    {
        "Meta": {"name": "Test Dashboard", "slug": "test-dashboard"},
        "components": [
            {
                "group": None,
                "groupWidth": None,
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
                "width": 12,
            },
            {
                "group": None,
                "groupWidth": None,
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
                "width": 12,
            },
        ],
    },
    {
        "Meta": {"name": "Test Complex Dashboard", "slug": "test-complex-dashboard"},
        "components": [
            {
                "group": None,
                "groupWidth": None,
                "isDeferred": True,
                "key": "component_3",
                "renderType": "Text",
                "value": None,
                "width": 12,
            },
            {
                "group": None,
                "groupWidth": None,
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
                "width": 12,
            },
            {
                "group": None,
                "groupWidth": None,
                "isDeferred": False,
                "key": "component_4",
                "renderType": "HTML",
                "value": "<div></div>",
                "width": 12,
            },
            {
                "group": None,
                "groupWidth": None,
                "isDeferred": False,
                "key": "component_5",
                "renderType": "Table",
                "value": {
                    "headers": ["a", "b"],
                    "last_page": 1,
                    "rows": [{"a": "Value", "b": "Value b"}],
                },
                "width": 12,
            },
            {
                "group": None,
                "groupWidth": None,
                "isDeferred": False,
                "key": "component_6",
                "renderType": "Chart",
                "value": {
                    "data": [
                        {
                            "marker": {},
                            "mode": None,
                            "name": None,
                            "text": None,
                            "type": None,
                            "x": ["a"],
                            "y": ["b"],
                        }
                    ],
                    "layout": {},
                },
                "width": 12,
            },
            {
                "group": None,
                "groupWidth": None,
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
                "width": 12,
            },
        ],
    },
]

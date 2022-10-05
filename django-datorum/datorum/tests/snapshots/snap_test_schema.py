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
    "Meta": {"layoutJson": None, "name": "Test Dashboard", "slug": "test-dashboard"},
    "components": [
        {
            "isDeferred": False,
            "key": "component_1",
            "renderType": "Text",
            "value": "value",
            "width": 6,
        },
        {
            "isDeferred": True,
            "key": "component_2",
            "renderType": "Text",
            "value": None,
            "width": 6,
        },
        {
            "isDeferred": False,
            "key": "component_3",
            "renderType": "Text",
            "value": "value from callable",
            "width": 6,
        },
    ],
}

snapshots["test_view__dashboard__not_found 1"] = None

snapshots["test_view__dashboard__with_layout 1"] = {
    "Meta": {
        "layoutJson": {
            "layout_components": [
                {
                    "layout_components": [
                        {
                            "css_classes": "css_style",
                            "layout_components": ["component_1"],
                            "renderType": "Div",
                            "width": 99,
                        },
                        {
                            "css_classes": "css_style",
                            "layout_components": ["component_2"],
                            "renderType": "Div",
                        },
                    ],
                    "renderType": "Div",
                }
            ]
        },
        "name": "Test Dashboard with Layout",
        "slug": "test-dashboard-with-layout",
    },
    "components": [
        {
            "isDeferred": False,
            "key": "component_1",
            "renderType": "Text",
            "value": "value",
            "width": 6,
        },
        {
            "isDeferred": True,
            "key": "component_2",
            "renderType": "Text",
            "value": None,
            "width": 6,
        },
        {
            "isDeferred": False,
            "key": "component_3",
            "renderType": "Text",
            "value": "value from callable",
            "width": 6,
        },
    ],
}

snapshots["test_view__dashboards 1"] = [
    {
        "Meta": {"name": "Test Model Dashboard", "slug": "test-model-dashboard"},
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
                "width": 6,
            }
        ],
    },
    {
        "Meta": {"name": "Test Admin Dashboard", "slug": "test-admin-dashboard"},
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "admin value",
                "width": 6,
            }
        ],
    },
    {
        "Meta": {"name": "Test Dashboard", "slug": "test-dashboard"},
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
                "width": 6,
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
                "width": 6,
            },
            {
                "isDeferred": False,
                "key": "component_3",
                "renderType": "Text",
                "value": "value from callable",
                "width": 6,
            },
        ],
    },
    {
        "Meta": {"name": "Test Complex Dashboard", "slug": "test-complex-dashboard"},
        "components": [
            {
                "isDeferred": True,
                "key": "component_3",
                "renderType": "Text",
                "value": None,
                "width": 6,
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
                "width": 6,
            },
            {
                "isDeferred": False,
                "key": "component_4",
                "renderType": "Text",
                "value": "<div></div>",
                "width": 6,
            },
            {
                "isDeferred": False,
                "key": "component_5",
                "renderType": "Table",
                "value": {
                    "data": [{"a": "Value", "b": "Value b"}],
                    "draw": 0,
                    "paging": None,
                    "recordsFiltered": 0,
                    "recordsTotal": 0,
                },
                "width": 6,
            },
            {
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
                "width": 6,
            },
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
                "width": 6,
            },
        ],
    },
    {
        "Meta": {
            "name": "Test Dashboard with Layout",
            "slug": "test-dashboard-with-layout",
        },
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
                "width": 6,
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
                "width": 6,
            },
            {
                "isDeferred": False,
                "key": "component_3",
                "renderType": "Text",
                "value": "value from callable",
                "width": 6,
            },
        ],
    },
]

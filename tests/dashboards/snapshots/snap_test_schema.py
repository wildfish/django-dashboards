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
        },
        {"isDeferred": True, "key": "component_2", "renderType": "Text", "value": None},
        {
            "isDeferred": False,
            "key": "component_3",
            "renderType": "Text",
            "value": "value from callable",
        },
    ],
}

snapshots["test_view__dashboard__with_layout 1"] = {
    "Meta": {
        "layoutJson": {
            "component_context": {},
            "layout_components": [
                {"html": "<hr />", "renderType": "HR"},
                {
                    "component_context": {},
                    "layout_components": [
                        {
                            "component_context": {},
                            "css_classes": "css_style",
                            "layout_components": ["component_1"],
                            "renderType": "Div",
                        },
                        {
                            "component_context": {},
                            "css_classes": "css_style",
                            "layout_components": ["component_2"],
                            "renderType": "Div",
                        },
                    ],
                    "renderType": "Div",
                },
            ],
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
        },
        {"isDeferred": True, "key": "component_2", "renderType": "Text", "value": None},
        {
            "isDeferred": False,
            "key": "component_3",
            "renderType": "Text",
            "value": "value from callable",
        },
    ],
}

snapshots["test_view__dashboards 1"] = [
    {
        "Meta": {"name": "Test Dashboard", "slug": "test-dashboard"},
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
            },
            {
                "isDeferred": False,
                "key": "component_3",
                "renderType": "Text",
                "value": "value from callable",
            },
        ],
    },
    {
        "Meta": {"name": "Test Filter Dashboard", "slug": "test-filter-dashboard"},
        "components": [
            {
                "isDeferred": False,
                "key": "filter_component",
                "renderType": "Form",
                "value": {
                    "action": "/app1/testfilterdashboard/filter_component-form/",
                    "dependents": ["dependent_component_1", "dependent_component_2"],
                    "form": [
                        {
                            "choices": [("all", "All"), ("one", "one"), ("two", "two")],
                            "field_type": "Select",
                            "help_text": "",
                            "id": "id_country",
                            "label": "Country",
                            "name": "country",
                            "required": True,
                            "value": "",
                        }
                    ],
                    "method": "get",
                },
            },
            {
                "isDeferred": False,
                "key": "dependent_component_1",
                "renderType": "Text",
                "value": "filter=None",
            },
            {
                "isDeferred": False,
                "key": "dependent_component_2",
                "renderType": "Text",
                "value": "filter=None",
            },
            {
                "isDeferred": False,
                "key": "non_dependent_component_3",
                "renderType": "Text",
                "value": "A value",
            },
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
            }
        ],
    },
    {
        "Meta": {"name": "Test Complex Dashboard", "slug": "test-complex-dashboard"},
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
            },
            {
                "isDeferred": True,
                "key": "component_3",
                "renderType": "Text",
                "value": None,
            },
            {
                "isDeferred": True,
                "key": "component_4",
                "renderType": "Text",
                "value": None,
            },
            {
                "isDeferred": False,
                "key": "component_5",
                "renderType": "Text",
                "value": "<div></div>",
            },
            {
                "isDeferred": False,
                "key": "component_6",
                "renderType": "Table",
                "value": {
                    "data": [{"a": "Value", "b": "Value b"}],
                    "draw": 0,
                    "filtered": 0,
                    "total": 0,
                },
            },
            {
                "isDeferred": False,
                "key": "component_7",
                "renderType": "Chart",
                "value": '{"data": [{"x": ["a"], "y": ["b"]}], "layout": {}}',
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
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
            },
            {
                "isDeferred": False,
                "key": "component_3",
                "renderType": "Text",
                "value": "value from callable",
            },
        ],
    },
    {
        "Meta": {"name": "Test Model Dashboard", "slug": "test-model-dashboard"},
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
            }
        ],
    },
]

snapshots["test_view__dashboards__no_permission 1"] = [
    {
        "Meta": {"name": "Test Filter Dashboard", "slug": "test-filter-dashboard"},
        "components": [
            {
                "isDeferred": False,
                "key": "filter_component",
                "renderType": "Form",
                "value": {
                    "action": "/app1/testfilterdashboard/filter_component-form/",
                    "dependents": ["dependent_component_1", "dependent_component_2"],
                    "form": [
                        {
                            "choices": [("all", "All"), ("one", "one"), ("two", "two")],
                            "field_type": "Select",
                            "help_text": "",
                            "id": "id_country",
                            "label": "Country",
                            "name": "country",
                            "required": True,
                            "value": "",
                        }
                    ],
                    "method": "get",
                },
            },
            {
                "isDeferred": False,
                "key": "dependent_component_1",
                "renderType": "Text",
                "value": "filter=None",
            },
            {
                "isDeferred": False,
                "key": "dependent_component_2",
                "renderType": "Text",
                "value": "filter=None",
            },
            {
                "isDeferred": False,
                "key": "non_dependent_component_3",
                "renderType": "Text",
                "value": "A value",
            },
        ],
    },
    {
        "Meta": {"name": "Test Complex Dashboard", "slug": "test-complex-dashboard"},
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
            },
            {
                "isDeferred": True,
                "key": "component_3",
                "renderType": "Text",
                "value": None,
            },
            {
                "isDeferred": True,
                "key": "component_4",
                "renderType": "Text",
                "value": None,
            },
            {
                "isDeferred": False,
                "key": "component_5",
                "renderType": "Text",
                "value": "<div></div>",
            },
            {
                "isDeferred": False,
                "key": "component_6",
                "renderType": "Table",
                "value": {
                    "data": [{"a": "Value", "b": "Value b"}],
                    "draw": 0,
                    "filtered": 0,
                    "total": 0,
                },
            },
            {
                "isDeferred": False,
                "key": "component_7",
                "renderType": "Chart",
                "value": '{"data": [{"x": ["a"], "y": ["b"]}], "layout": {}}',
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
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
            },
            {
                "isDeferred": False,
                "key": "component_3",
                "renderType": "Text",
                "value": "value from callable",
            },
        ],
    },
    {
        "Meta": {"name": "Test Model Dashboard", "slug": "test-model-dashboard"},
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
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
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
            },
            {
                "isDeferred": False,
                "key": "component_3",
                "renderType": "Text",
                "value": "value from callable",
            },
        ],
    },
    {
        "Meta": {"name": "ExtraDashboard", "slug": "extradashboard"},
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
            },
            {
                "isDeferred": False,
                "key": "component_3",
                "renderType": "Text",
                "value": "value from callable",
            },
        ],
    },
    {
        "Meta": {"name": "GQLDashboard", "slug": "gqldashboard"},
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
            },
            {
                "isDeferred": False,
                "key": "component_3",
                "renderType": "Text",
                "value": "value from callable",
            },
        ],
    },
]

snapshots["test_view__dashboards__permission 1"] = [
    {
        "Meta": {"name": "Test Dashboard", "slug": "test-dashboard"},
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
            },
            {
                "isDeferred": False,
                "key": "component_3",
                "renderType": "Text",
                "value": "value from callable",
            },
        ],
    },
    {
        "Meta": {"name": "Test Filter Dashboard", "slug": "test-filter-dashboard"},
        "components": [
            {
                "isDeferred": False,
                "key": "filter_component",
                "renderType": "Form",
                "value": {
                    "action": "/app1/testfilterdashboard/filter_component-form/",
                    "dependents": ["dependent_component_1", "dependent_component_2"],
                    "form": [
                        {
                            "choices": [("all", "All"), ("one", "one"), ("two", "two")],
                            "field_type": "Select",
                            "help_text": "",
                            "id": "id_country",
                            "label": "Country",
                            "name": "country",
                            "required": True,
                            "value": "",
                        }
                    ],
                    "method": "get",
                },
            },
            {
                "isDeferred": False,
                "key": "dependent_component_1",
                "renderType": "Text",
                "value": "filter=None",
            },
            {
                "isDeferred": False,
                "key": "dependent_component_2",
                "renderType": "Text",
                "value": "filter=None",
            },
            {
                "isDeferred": False,
                "key": "non_dependent_component_3",
                "renderType": "Text",
                "value": "A value",
            },
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
            }
        ],
    },
    {
        "Meta": {"name": "Test Complex Dashboard", "slug": "test-complex-dashboard"},
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
            },
            {
                "isDeferred": True,
                "key": "component_3",
                "renderType": "Text",
                "value": None,
            },
            {
                "isDeferred": True,
                "key": "component_4",
                "renderType": "Text",
                "value": None,
            },
            {
                "isDeferred": False,
                "key": "component_5",
                "renderType": "Text",
                "value": "<div></div>",
            },
            {
                "isDeferred": False,
                "key": "component_6",
                "renderType": "Table",
                "value": {
                    "data": [{"a": "Value", "b": "Value b"}],
                    "draw": 0,
                    "filtered": 0,
                    "total": 0,
                },
            },
            {
                "isDeferred": False,
                "key": "component_7",
                "renderType": "Chart",
                "value": '{"data": [{"x": ["a"], "y": ["b"]}], "layout": {}}',
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
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
            },
            {
                "isDeferred": False,
                "key": "component_3",
                "renderType": "Text",
                "value": "value from callable",
            },
        ],
    },
    {
        "Meta": {"name": "Test Model Dashboard", "slug": "test-model-dashboard"},
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
            }
        ],
    },
]

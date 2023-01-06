# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots["test_view__component__deferred 1"] = {"isDeferred": True, "value": "value"}

snapshots["test_view__component__not_deferred 1"] = {
    "isDeferred": False,
    "value": "value",
}

snapshots["test_view__dashboard 1"] = {
    "Meta": {
        "layoutJson": None,
        "name": "Test Dashboard",
        "slug": "test-dashboard",
        "verboseName": "Test Dashboard",
    },
    "components": [
        {
            "isDeferred": False,
            "key": "component_1",
            "renderType": "Text",
            "value": "value",
            "verboseName": "component_1",
        },
        {
            "isDeferred": True,
            "key": "component_2",
            "renderType": "Text",
            "value": None,
            "verboseName": "component_2",
        },
        {
            "isDeferred": False,
            "key": "component_3",
            "renderType": "Text",
            "value": "value from callable",
            "verboseName": "Callable value component",
        },
    ],
}

snapshots["test_view__dashboard__with_layout 1"] = {
    "Meta": {
        "layoutJson": {
            "component_context": {},
            "grid_css_classes": "span-6",
            "layout_components": [
                {"html": "<hr />", "renderType": "HR"},
                {
                    "component_context": {},
                    "grid_css_classes": "span-6",
                    "layout_components": [
                        {
                            "component_context": {},
                            "css_classes": "css_style",
                            "grid_css_classes": "span-6",
                            "layout_components": ["component_1"],
                            "renderType": "Div",
                        },
                        {
                            "component_context": {},
                            "css_classes": "css_style",
                            "grid_css_classes": "span-6",
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
        "verboseName": "Test Dashboard with Layout",
    },
    "components": [
        {
            "isDeferred": False,
            "key": "component_1",
            "renderType": "Text",
            "value": "value",
            "verboseName": "component_1",
        },
        {
            "isDeferred": True,
            "key": "component_2",
            "renderType": "Text",
            "value": None,
            "verboseName": "component_2",
        },
        {
            "isDeferred": False,
            "key": "component_3",
            "renderType": "Text",
            "value": "value from callable",
            "verboseName": "Callable value component",
        },
    ],
}

snapshots["test_view__dashboards 1"] = [
    {
        "Meta": {
            "name": "Test Dashboard",
            "slug": "test-dashboard",
            "verboseName": "Test Dashboard",
        },
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
                "verboseName": "component_1",
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
                "verboseName": "component_2",
            },
            {
                "isDeferred": False,
                "key": "component_3",
                "renderType": "Text",
                "value": "value from callable",
                "verboseName": "Callable value component",
            },
        ],
    },
    {
        "Meta": {
            "name": "Test Filter Dashboard",
            "slug": "test-filter-dashboard",
            "verboseName": "Test Filter Dashboard",
        },
        "components": [
            {
                "isDeferred": False,
                "key": "filter_component",
                "renderType": "Form",
                "value": {
                    "action": "/app1/testfilterdashboard/filter_component/@form/",
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
                "verboseName": "filter_component",
            },
            {
                "isDeferred": False,
                "key": "dependent_component_1",
                "renderType": "Text",
                "value": "filter=None",
                "verboseName": "dependent_component_1",
            },
            {
                "isDeferred": False,
                "key": "dependent_component_2",
                "renderType": "Text",
                "value": "filter=None",
                "verboseName": "dependent_component_2",
            },
            {
                "isDeferred": False,
                "key": "non_dependent_component_3",
                "renderType": "Text",
                "value": "A value",
                "verboseName": "non_dependent_component_3",
            },
        ],
    },
    {
        "Meta": {
            "name": "Test Admin Dashboard",
            "slug": "test-admin-dashboard",
            "verboseName": "Test Admin Dashboard",
        },
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "admin value",
                "verboseName": "component_1",
            }
        ],
    },
    {
        "Meta": {
            "name": "Test Complex Dashboard",
            "slug": "test-complex-dashboard",
            "verboseName": "Test Complex Dashboard",
        },
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
                "verboseName": "component_1",
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
                "verboseName": "component_2",
            },
            {
                "isDeferred": True,
                "key": "component_3",
                "renderType": "Text",
                "value": None,
                "verboseName": "component_3",
            },
            {
                "isDeferred": True,
                "key": "component_4",
                "renderType": "Text",
                "value": None,
                "verboseName": "component_4",
            },
            {
                "isDeferred": False,
                "key": "component_5",
                "renderType": "Text",
                "value": "<div></div>",
                "verboseName": "component_5",
            },
            {
                "isDeferred": False,
                "key": "component_6",
                "renderType": "Table",
                "value": {
                    "columns": {"a": "A", "b": "B"},
                    "columns_datatables": [
                        {"data": "a", "title": "A"},
                        {"data": "b", "title": "B"},
                    ],
                    "data": [{"a": "Value", "b": "Value b"}],
                    "draw": 1,
                    "filtered": 1,
                    "total": 1,
                },
                "verboseName": "component_6",
            },
            {
                "isDeferred": False,
                "key": "component_7",
                "renderType": "Chart",
                "value": '{"data": [{"x": ["a"], "y": ["b"]}], "layout": {}}',
                "verboseName": "component_7",
            },
        ],
    },
    {
        "Meta": {
            "name": "Test Dashboard with Layout",
            "slug": "test-dashboard-with-layout",
            "verboseName": "Test Dashboard with Layout",
        },
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
                "verboseName": "component_1",
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
                "verboseName": "component_2",
            },
            {
                "isDeferred": False,
                "key": "component_3",
                "renderType": "Text",
                "value": "value from callable",
                "verboseName": "Callable value component",
            },
        ],
    },
    {
        "Meta": {
            "name": "TestNoMetaDashboard",
            "slug": "testnometadashboard",
            "verboseName": "TestNoMetaDashboard",
        },
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
                "verboseName": "component_1",
            }
        ],
    },
]

snapshots["test_view__dashboards__no_permission 1"] = [
    {
        "Meta": {
            "name": "Test Dashboard",
            "slug": "test-dashboard",
            "verboseName": "Test Dashboard",
        },
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
                "verboseName": "component_1",
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
                "verboseName": "component_2",
            },
            {
                "isDeferred": False,
                "key": "component_3",
                "renderType": "Text",
                "value": "value from callable",
                "verboseName": "Callable value component",
            },
        ],
    },
    {
        "Meta": {
            "name": "Test Filter Dashboard",
            "slug": "test-filter-dashboard",
            "verboseName": "Test Filter Dashboard",
        },
        "components": [
            {
                "isDeferred": False,
                "key": "filter_component",
                "renderType": "Form",
                "value": {
                    "action": "/app1/testfilterdashboard/filter_component/@form/",
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
                "verboseName": "filter_component",
            },
            {
                "isDeferred": False,
                "key": "dependent_component_1",
                "renderType": "Text",
                "value": "filter=None",
                "verboseName": "dependent_component_1",
            },
            {
                "isDeferred": False,
                "key": "dependent_component_2",
                "renderType": "Text",
                "value": "filter=None",
                "verboseName": "dependent_component_2",
            },
            {
                "isDeferred": False,
                "key": "non_dependent_component_3",
                "renderType": "Text",
                "value": "A value",
                "verboseName": "non_dependent_component_3",
            },
        ],
    },
    {
        "Meta": {
            "name": "Test Complex Dashboard",
            "slug": "test-complex-dashboard",
            "verboseName": "Test Complex Dashboard",
        },
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
                "verboseName": "component_1",
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
                "verboseName": "component_2",
            },
            {
                "isDeferred": True,
                "key": "component_3",
                "renderType": "Text",
                "value": None,
                "verboseName": "component_3",
            },
            {
                "isDeferred": True,
                "key": "component_4",
                "renderType": "Text",
                "value": None,
                "verboseName": "component_4",
            },
            {
                "isDeferred": False,
                "key": "component_5",
                "renderType": "Text",
                "value": "<div></div>",
                "verboseName": "component_5",
            },
            {
                "isDeferred": False,
                "key": "component_6",
                "renderType": "Table",
                "value": {
                    "columns": {"a": "A", "b": "B"},
                    "columns_datatables": [
                        {"data": "a", "title": "A"},
                        {"data": "b", "title": "B"},
                    ],
                    "data": [{"a": "Value", "b": "Value b"}],
                    "draw": 1,
                    "filtered": 1,
                    "total": 1,
                },
                "verboseName": "component_6",
            },
            {
                "isDeferred": False,
                "key": "component_7",
                "renderType": "Chart",
                "value": '{"data": [{"x": ["a"], "y": ["b"]}], "layout": {}}',
                "verboseName": "component_7",
            },
        ],
    },
    {
        "Meta": {
            "name": "Test Dashboard with Layout",
            "slug": "test-dashboard-with-layout",
            "verboseName": "Test Dashboard with Layout",
        },
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
                "verboseName": "component_1",
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
                "verboseName": "component_2",
            },
            {
                "isDeferred": False,
                "key": "component_3",
                "renderType": "Text",
                "value": "value from callable",
                "verboseName": "Callable value component",
            },
        ],
    },
    {
        "Meta": {
            "name": "TestNoMetaDashboard",
            "slug": "testnometadashboard",
            "verboseName": "TestNoMetaDashboard",
        },
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
                "verboseName": "component_1",
            }
        ],
    },
]

snapshots["test_view__dashboards__permission 1"] = [
    {
        "Meta": {
            "name": "Test Dashboard",
            "slug": "test-dashboard",
            "verboseName": "Test Dashboard",
        },
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
                "verboseName": "component_1",
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
                "verboseName": "component_2",
            },
            {
                "isDeferred": False,
                "key": "component_3",
                "renderType": "Text",
                "value": "value from callable",
                "verboseName": "Callable value component",
            },
        ],
    },
    {
        "Meta": {
            "name": "Test Filter Dashboard",
            "slug": "test-filter-dashboard",
            "verboseName": "Test Filter Dashboard",
        },
        "components": [
            {
                "isDeferred": False,
                "key": "filter_component",
                "renderType": "Form",
                "value": {
                    "action": "/app1/testfilterdashboard/filter_component/@form/",
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
                "verboseName": "filter_component",
            },
            {
                "isDeferred": False,
                "key": "dependent_component_1",
                "renderType": "Text",
                "value": "filter=None",
                "verboseName": "dependent_component_1",
            },
            {
                "isDeferred": False,
                "key": "dependent_component_2",
                "renderType": "Text",
                "value": "filter=None",
                "verboseName": "dependent_component_2",
            },
            {
                "isDeferred": False,
                "key": "non_dependent_component_3",
                "renderType": "Text",
                "value": "A value",
                "verboseName": "non_dependent_component_3",
            },
        ],
    },
    {
        "Meta": {
            "name": "Test Admin Dashboard",
            "slug": "test-admin-dashboard",
            "verboseName": "Test Admin Dashboard",
        },
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "admin value",
                "verboseName": "component_1",
            }
        ],
    },
    {
        "Meta": {
            "name": "Test Complex Dashboard",
            "slug": "test-complex-dashboard",
            "verboseName": "Test Complex Dashboard",
        },
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
                "verboseName": "component_1",
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
                "verboseName": "component_2",
            },
            {
                "isDeferred": True,
                "key": "component_3",
                "renderType": "Text",
                "value": None,
                "verboseName": "component_3",
            },
            {
                "isDeferred": True,
                "key": "component_4",
                "renderType": "Text",
                "value": None,
                "verboseName": "component_4",
            },
            {
                "isDeferred": False,
                "key": "component_5",
                "renderType": "Text",
                "value": "<div></div>",
                "verboseName": "component_5",
            },
            {
                "isDeferred": False,
                "key": "component_6",
                "renderType": "Table",
                "value": {
                    "columns": {"a": "A", "b": "B"},
                    "columns_datatables": [
                        {"data": "a", "title": "A"},
                        {"data": "b", "title": "B"},
                    ],
                    "data": [{"a": "Value", "b": "Value b"}],
                    "draw": 1,
                    "filtered": 1,
                    "total": 1,
                },
                "verboseName": "component_6",
            },
            {
                "isDeferred": False,
                "key": "component_7",
                "renderType": "Chart",
                "value": '{"data": [{"x": ["a"], "y": ["b"]}], "layout": {}}',
                "verboseName": "component_7",
            },
        ],
    },
    {
        "Meta": {
            "name": "Test Dashboard with Layout",
            "slug": "test-dashboard-with-layout",
            "verboseName": "Test Dashboard with Layout",
        },
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
                "verboseName": "component_1",
            },
            {
                "isDeferred": True,
                "key": "component_2",
                "renderType": "Text",
                "value": None,
                "verboseName": "component_2",
            },
            {
                "isDeferred": False,
                "key": "component_3",
                "renderType": "Text",
                "value": "value from callable",
                "verboseName": "Callable value component",
            },
        ],
    },
    {
        "Meta": {
            "name": "TestNoMetaDashboard",
            "slug": "testnometadashboard",
            "verboseName": "TestNoMetaDashboard",
        },
        "components": [
            {
                "isDeferred": False,
                "key": "component_1",
                "renderType": "Text",
                "value": "value",
                "verboseName": "component_1",
            }
        ],
    },
]

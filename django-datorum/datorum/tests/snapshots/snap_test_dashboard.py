# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test__get_attributes_order 1"] = [
    "__module__",
    "component_1",
    "component_2",
    "Meta",
    "__doc__",
    "__module__",
    "__annotations__",
    "include_in_graphql",
    "permission_classes",
    "__init__",
    "get_context",
    "get_attributes_order",
    "get_components",
    "get_dashboard_permissions",
    "has_permissions",
    "get_urls",
    "urls",
    "Meta",
    "__str__",
    "__getitem__",
    "__doc__",
]

snapshots["test__get_attributes_order__with_parent 1"] = [
    "__module__",
    "component_3",
    "component_2",
    "component_4",
    "Meta",
    "__doc__",
    "__module__",
    "component_1",
    "component_2",
    "Meta",
    "__doc__",
    "__module__",
    "__annotations__",
    "include_in_graphql",
    "permission_classes",
    "__init__",
    "get_context",
    "get_attributes_order",
    "get_components",
    "get_dashboard_permissions",
    "has_permissions",
    "get_urls",
    "urls",
    "Meta",
    "__str__",
    "__getitem__",
    "__doc__",
]

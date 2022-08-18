# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots["test__get_attributes_order 1"] = [
    "__module__",
    "component_1",
    "component_2",
    "__doc__",
    "__module__",
    "__init__",
    "get_context",
    "get_attributes_order",
    "get_components",
    "Meta",
    "__doc__",
]

snapshots["test__get_attributes_order__with_parent 1"] = [
    "__module__",
    "component_3",
    "component_2",
    "component_4",
    "__doc__",
    "__module__",
    "component_1",
    "component_2",
    "__doc__",
    "__module__",
    "__init__",
    "get_context",
    "get_attributes_order",
    "get_components",
    "Meta",
    "__doc__",
]

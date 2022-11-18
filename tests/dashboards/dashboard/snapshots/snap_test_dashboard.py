# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots["test__get_attributes_order 1"] = GenericRepr(
    "dict_keys(['component_1', 'component_2', 'component_3'])"
)

snapshots["test__get_attributes_order__with_parent 1"] = GenericRepr(
    "dict_keys(['component_1', 'component_2', 'component_3', 'component_4', 'component_5', 'component_6', 'component_7'])"
)

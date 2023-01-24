# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_log_list__tasks_completed 1"
] = """[20/Dec/2022 13:23:55]: Done
[20/Dec/2022 13:23:55]: Done
[20/Dec/2022 13:23:55]: Done"""

# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_cta_component__renders_value[False] 1"
] = """


    <a href="/">
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            
click here

        </div>
    </a>


"""

snapshots[
    "test_cta_component__renders_value[True] 1"
] = """


    <a href="/">
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            
click here

        </div>
    </a>


"""

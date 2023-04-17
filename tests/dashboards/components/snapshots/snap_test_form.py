# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_form_component__renders_value[False] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <form hx-get="/dash/app1/testdashboard/test/@form/?key=dashapp1testdashboardcomponenttest" hx-trigger="change" hx-swap="outerHTML" hx-target="#component-dashapp1testdashboardcomponenttest-inner"><table class="table form-table"><tbody><tr><th><label for="id_number">Number:</label></th><td><select name="number" id="id_number"><option value="one">one</option><option value="two">two</option><option value="three">three</option></select></td></tr></tbody></table></form>
        </div>
    


"""

snapshots[
    "test_form_component__renders_value[True] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <form hx-get="/dash/app1/testdashboard/test/@form/?key=dashapp1testdashboardcomponenttest" hx-trigger="change" hx-swap="outerHTML" hx-target="#component-dashapp1testdashboardcomponenttest-inner"><table class="table form-table"><tbody><tr><th><label for="id_number">Number:</label></th><td><select name="number" id="id_number"><option value="one">one</option><option value="two">two</option><option value="three">three</option></select></td></tr></tbody></table></form>
        </div>
    


"""

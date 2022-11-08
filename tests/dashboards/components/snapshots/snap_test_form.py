# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_form_component__renders_value[False] 1"
] = """



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <form hx-get="/app1/testdashboard/test-form/?key=test" hx-trigger="change" hx-swap="outerHTML" hx-target="#component-test-inner">
  <p>
    <label for="id_number">Number:</label>
    <select name="number" id="id_number">
  <option value="one">one</option>

  <option value="two">two</option>

  <option value="three">three</option>

</select>
    
    
      
    
  </p>
</form>
    </div>
"""

snapshots[
    "test_form_component__renders_value[True] 1"
] = """



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <form hx-get="/app1/testdashboard/test-form/?key=test" hx-trigger="change" hx-swap="outerHTML" hx-target="#component-test-inner">
  <p>
    <label for="id_number">Number:</label>
    <select name="number" id="id_number">
  <option value="one">one</option>

  <option value="two">two</option>

  <option value="three">three</option>

</select>
    
    
      
    
  </p>
</form>
    </div>
"""

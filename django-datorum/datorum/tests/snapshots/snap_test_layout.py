# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_dashboard__render_layout 1"
] = """

<!DOCTYPE html>
<html lang="en">
<head>
    <title>Datorum | Test Dashboard with Layout</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <script src="/static/js/htmx.min.js"></script>
    <script src="/static/js/alpine-3.10.3.js" defer></script>
    <script src="/static/js/plotly-2.12.1.min.js"></script>
    <script src="/static/js/tabulator.min.js"></script>

    <link rel="stylesheet" href="/static/css/tabulator.min.css">
    <link rel="stylesheet" href="/static/css/styles.css">
    
</head>
<body class="">
    
    <div class="menu"></div>
    <h1>
  Test Dashboard with Layout
</h1>
    <div class="content">
        
    <div class="span-6 None">
  <div class="span-6 css_style">
  
    


    
    <div id="component-component_1-inner" class="dashboard-component-inner fade-in">
        
value

    </div>

</div><div class="span-6 css_style">
  
    <div hx-get="/TestDashboardWithLayout/component_2/?key=component_2" hx-trigger="intersect once"></div>

</div>
</div>

    </div>
    
    
    
</body>
</html>"""

snapshots["test_html__render 1"] = "some text...."

snapshots[
    "test_html_component__render[Card] 1"
] = """<div class="span-6 css_class">
  
  <div class="card-body">
    
    


    
    <div id="component-component_1-inner" class="dashboard-component-inner fade-in">
        
value

    </div>

  </div>
</div>"""

snapshots[
    "test_html_component__render[Div] 1"
] = """<div class="span-6 css_class">
  
    


    
    <div id="component-component_1-inner" class="dashboard-component-inner fade-in">
        
value

    </div>

</div>"""

snapshots[
    "test_html_component__render[Tab] 1"
] = """<div x-show="tab === \'\'">
    <div class="span-6 css_class">
  
    


    
    <div id="component-component_1-inner" class="dashboard-component-inner fade-in">
        
value

    </div>

</div>
</div>"""

snapshots[
    "test_layout_component__render 1"
] = """
    


    
    <div id="component-component_1-inner" class="dashboard-component-inner fade-in">
        
value

    </div>

    <div hx-get="/TestDashboard/component_2/?key=component_2" hx-trigger="intersect once"></div>
"""

snapshots[
    "test_layout_component__unknown_component_ignored 1"
] = """
    


    
    <div id="component-component_1-inner" class="dashboard-component-inner fade-in">
        
value

    </div>

    <div hx-get="/TestDashboard/component_2/?key=component_2" hx-trigger="intersect once"></div>
"""

snapshots[
    "test_tab_container__render 1"
] = """<div x-data="{ tab: \'\' }">
    <ul id="" class="tabs" >
        <li class="tab-link">
  <a :class="{ \'active\': tab === \'\' }" x-on:click.prevent="tab = \'\'" href="#">
    
  </a>
</li>
    </ul>

    <div class="">
        <div x-show="tab === \'\'">
    <div class="span-6 tab-pane fade">
  some text....
</div>
</div>
    </div>
</div>"""

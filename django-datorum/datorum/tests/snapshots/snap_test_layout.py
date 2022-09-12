# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_dashboard__render_layout 1'] = '''

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
        
    Some text.....<div class="div " id="wrapper">
  <div class="div css_style" id="c1">
  
    


    
    <div id="component-component_1-inner" class="dashboard-component-inner fade-in">
        value

        
    </div>

</div><div class="div css_style" id="c2">
  
    <div hx-get="/TestDashboardWithLayout/component_2/?key=component_2" hx-trigger="load"></div>

</div>
</div>

    </div>
    
    
    
</body>
</html>'''

snapshots['test_html__render 1'] = 'some text....'

snapshots['test_html_component__render[Card] 1'] = '''<div class="card css_class">
  
  <div class="card-body">
    
    


    
    <div id="component-component_1-inner" class="dashboard-component-inner fade-in">
        value

        
    </div>

  </div>
</div>'''

snapshots['test_html_component__render[Div] 1'] = '''<div class="div css_class" id="e1">
  
    


    
    <div id="component-component_1-inner" class="dashboard-component-inner fade-in">
        value

        
    </div>

</div>'''

snapshots['test_html_component__render[Tab] 1'] = '''<div class="tab-pane fade css_class" id="e1">
  
</div>'''

snapshots['test_layout_component__render 1'] = '''
    


    
    <div id="component-component_1-inner" class="dashboard-component-inner fade-in">
        value

        
    </div>

    <div hx-get="/TestDashboard/component_2/?key=component_2" hx-trigger="load"></div>
'''

snapshots['test_layout_component__unknown_component_ignored 1'] = '''
    


    
    <div id="component-component_1-inner" class="dashboard-component-inner fade-in">
        value

        
    </div>

    <div hx-get="/TestDashboard/component_2/?key=component_2" hx-trigger="load"></div>
'''

snapshots['test_tab_container__render 1'] = '''<ul id="e2" class="nav nav-tabs">
    <li class="nav-item">
  <a class="nav-link active" href="#e1" data-toggle="tab">
    &lt;datorum.layout.HTML object at 0x296019b20&gt;</a>
</li>
</ul>
<div class="tab-content ">
    <div class="tab-pane fade  show active" id="e1">
  
</div>
</div>'''

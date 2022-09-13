# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_view__get__all 1"
] = """

<!DOCTYPE html>
<html lang="en">
<head>
    <title>Datorum | Test Dashboard</title>
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
  Test Dashboard
</h1>
    <div class="content">
        
    

  
  
  
    
    <div class="dashboard-container">
      
      
        
          
            <div id="component-component_1"
                 class="dashboard-component span-12 grid-a
                                 None">
              
    


    
    <div id="component-component_1-inner" class="dashboard-component-inner fade-in">
        
value

    </div>

            </div>
          
            <div id="component-component_2"
                 class="dashboard-component span-12 grid-b
                                 None">
              
    <div hx-get="/TestDashboard/component_2/?key=component_2" hx-trigger="intersect once"></div>

            </div>
          
        
      
    </div>
    
  
  


    </div>
    
    
    
</body>
</html>"""

snapshots["test_view__get__json 1"] = b'"value"'

snapshots[
    "test_view__get__partial_template 1"
] = """


    


    
    <div id="component-component_2-inner" class="dashboard-component-inner fade-in">
        
value

    </div>



"""

# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_component_view__with_model 1"
] = """





    
    <div id="component-component_1-inner" class="dashboard-component-inner fade-in">
        
value

    </div>



"""

snapshots[
    "test_component_view__with_model 2"
] = """





    
    <div id="component-component_1-inner" class="dashboard-component-inner fade-in">
        
value

    </div>



"""

snapshots[
    "test_view__get__all 1"
] = """

<!DOCTYPE html>
<html lang="en">
<head>
    <title>Wildcoeus | Test Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <script src="/static/wildcoeus/js/htmx.min.js"></script>
    <script src="/static/wildcoeus/js/htmx.debug.min.js"></script>
    <script src="/static/wildcoeus/js/htmx.sse.min.js"></script>
    <script src="/static/wildcoeus/js/hyperscript-0.9.7.min.js"></script>
    <script src="/static/wildcoeus/js/alpine-3.10.3.js" defer></script>
    <script src="/static/wildcoeus/js/plotly-2.12.1.min.js"></script>

    <script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-3.5.1.js"></script>
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/v/dt/dt-1.12.1/fh-3.2.4/r-2.3.0/sc-2.0.7/sr-1.1.1/datatables.min.css"/>
    <script type="text/javascript" src="https://cdn.datatables.net/v/dt/dt-1.12.1/fh-3.2.4/r-2.3.0/sc-2.0.7/sr-1.1.1/datatables.min.js"></script>

    <link rel="stylesheet" href="/static/wildcoeus/css/styles.css">
    
</head>
<body class="" hx-headers=\'{"X-CSRFToken": "b4MWDYFcaH2l6objYxQU0W34HsDUy3oqkenyp0ngUaq64yQKnKtHESmWFiwy5dhg"}\'>
    
    <div class="menu"></div>
    <h1>
  Test Dashboard
</h1>
    <div class="content">
        
    <div class="span-6 ">
  <div class="card  dashboard-component">
    
    
    <div class="card-body">
      



    
    <div id="component-component_1-inner" class="dashboard-component-inner fade-in">
        
value

    </div>

    </div>
    
  </div>
</div><div class="span-6 ">
  <div class="card  dashboard-component">
    
    
    <div class="card-body">
      



    <div hx-get="/app1/testdashboard/component/component_2/"
         hx-trigger="intersect once delay:74ms"></div>

    </div>
    
  </div>
</div><div class="span-6 ">
  <div class="card  dashboard-component">
    
    
    <div class="card-body">
      



    
    <div id="component-component_3-inner" class="dashboard-component-inner fade-in">
        
value from callable

    </div>

    </div>
    
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

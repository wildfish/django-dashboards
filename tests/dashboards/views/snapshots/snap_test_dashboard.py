# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_get 1"
] = """<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Wildcoeus | Test Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        
    
    
<script src="/static/wildcoeus/vendor/js/htmx.min.js"></script>
<script src="/static/wildcoeus/vendor/js/alpine.min.js" defer></script>
<script src="/static/wildcoeus/vendor/js/plotly.min.js"></script>
<script src="/static/wildcoeus/vendor/js/jquery.min.js"></script>
<script src="/static/wildcoeus/vendor/js/datatables.min.js"></script>

        
    
    
<link rel="stylesheet" href="/static/wildcoeus/css/wildcoeus.css">
<link rel="stylesheet" href="/static/wildcoeus/vendor/css/datatables.min.css">


    </head>
    <body hx-headers=\'{"X-CSRFToken": "7vjLeUodP1W3pgKkcMiZ1CBoLK6WxvWLK4xnuUTdJd4KyeYCfhohibp8nFSlpDWi"}\'>
        
            
  Test Dashboard

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
         hx-trigger="intersect once delay:1ms"></div>

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

snapshots[
    "test_get__render 1"
] = """<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Wildcoeus | Test Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        
    
    
<script src="/static/wildcoeus/vendor/js/htmx.min.js"></script>
<script src="/static/wildcoeus/vendor/js/alpine.min.js" defer></script>
<script src="/static/wildcoeus/vendor/js/plotly.min.js"></script>
<script src="/static/wildcoeus/vendor/js/jquery.min.js"></script>
<script src="/static/wildcoeus/vendor/js/datatables.min.js"></script>

        
    
    
<link rel="stylesheet" href="/static/wildcoeus/css/wildcoeus.css">
<link rel="stylesheet" href="/static/wildcoeus/vendor/css/datatables.min.css">


    </head>
    <body hx-headers=\'{"X-CSRFToken": "5AiHhovtRkA7qY5SROE0ISxNSff7tv5fqXq5618ZDOcdG5YCrsEzfSZNCpYXeBZz"}\'>
        
            
  Test Dashboard

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
         hx-trigger="intersect once delay:1ms"></div>

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

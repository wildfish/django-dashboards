# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_stat_component__renders_value[False-component_kwargs0] 1"
] = """


    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="stat">
  
  
  <h2>100%</h2>
  <p class="stat__text">
    
    <span>increase</span>
  </p>
  
</div>
        </div>
    


"""

snapshots[
    "test_stat_component__renders_value[False-component_kwargs1] 1"
] = """


    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="stat">
  
  
  <h2>100%</h2>
  <p class="stat__text">
    
    <span>increase</span>
  </p>
  
</div>
        </div>
    


"""

snapshots[
    "test_stat_component__renders_value[False-component_kwargs2] 1"
] = """


    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="stat">
  
  
  <h2>100%</h2>
  <p class="stat__text">
    
    <span class="text-success">
    
      &uarr;
       Change
    </span>
    
    <span>increase</span>
  </p>
  
</div>
        </div>
    


"""

snapshots[
    "test_stat_component__renders_value[True-component_kwargs0] 1"
] = """


    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="stat">
  
  
  <h2>100%</h2>
  <p class="stat__text">
    
    <span>increase</span>
  </p>
  
</div>
        </div>
    


"""

snapshots[
    "test_stat_component__renders_value[True-component_kwargs1] 1"
] = """


    <div hx-get="/dash/app1/testdashboard/@component/test/"
         hx-trigger="intersect once delay:1ms">
        <div class="htmx-indicator">
            
<div class="loading-img">
    <img src="/static/dashboards/loading.svg" />
</div>
        </div>
    </div>


"""

snapshots[
    "test_stat_component__renders_value[True-component_kwargs2] 1"
] = """


    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="stat">
  
  
  <h2>100%</h2>
  <p class="stat__text">
    
    <span class="text-success">
    
      &uarr;
       Change
    </span>
    
    <span>increase</span>
  </p>
  
</div>
        </div>
    


"""

snapshots[
    "test_stat_component__renders_value__with_date_serializer[False] 1"
] = """


    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div id="dashapp1testdashboardcomponenttest" class="stat">
  <div class="stat__heading">
    <h2 class="stat__title">Users</h2>
    
  </div>
  <div class="stat__body">
    <p class="stat__text">
      0People
    </p>
    
    
      <p class="stat__change">
        <span class="positive">
        &uarr;
        100.0%
        </span>
        in 1\xa0week
      </p>
      
    
  </div>
</div>

<script>
  feather.replace();
</script>

        </div>
    


"""

snapshots[
    "test_stat_component__renders_value__with_date_serializer[True] 1"
] = """


    <div hx-get="/dash/app1/testdashboard/@component/test/"
         hx-trigger="intersect once delay:1ms">
        <div class="htmx-indicator">
            
<div class="loading-img">
    <img src="/static/dashboards/loading.svg" />
</div>
        </div>
    </div>


"""

snapshots[
    "test_stat_component__renders_value__with_serializer[False] 1"
] = """


    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div id="dashapp1testdashboardcomponenttest" class="stat">
  <div class="stat__heading">
    <h2 class="stat__title">Users</h2>
    
  </div>
  <div class="stat__body">
    <p class="stat__text">
      0People
    </p>
    
  </div>
</div>

        </div>
    


"""

snapshots[
    "test_stat_component__renders_value__with_serializer[True] 1"
] = """


    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div id="dashapp1testdashboardcomponenttest" class="stat">
  <div class="stat__heading">
    <h2 class="stat__title">Users</h2>
    
  </div>
  <div class="stat__body">
    <p class="stat__text">
      0People
    </p>
    
  </div>
</div>

        </div>
    


"""

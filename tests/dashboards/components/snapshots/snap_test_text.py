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

snapshots[
    "test_stat_component__renders_value[False-component_kwargs0] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="stat">
  
  
  <h2 class="stat__heading">100%</h2>
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
  
  
  <h2 class="stat__heading">100%</h2>
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
  
  
  <h2 class="stat__heading">100%</h2>
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
  
  
  <h2 class="stat__heading">100%</h2>
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
            Loading...
        </div>
    </div>


"""

snapshots[
    "test_stat_component__renders_value[True-component_kwargs2] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="stat">
  
  
  <h2 class="stat__heading">100%</h2>
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

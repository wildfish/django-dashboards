# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_cta_component__renders_value[False] 1"
] = """



    <a href="/">
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            
click here

        </div>
    </a>


"""

snapshots[
    "test_cta_component__renders_value[True] 1"
] = """



    <a href="/">
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            
click here

        </div>
    </a>


"""

snapshots[
    "test_progress_component__renders_value[False-component_kwargs0] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            

<div class="progress-w-percent">
  <strong class="progress-value">100%</strong>
  <div class="progress progress-sm">
    <div class="progress-bar" role="progressbar" style="width: 100%;" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100"></div>
  </div>
</div>

        </div>
    


"""

snapshots[
    "test_progress_component__renders_value[False-component_kwargs1] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            

<div class="progress-w-percent">
  <strong class="progress-value">100%</strong>
  <div class="progress progress-sm">
    <div class="progress-bar" role="progressbar" style="width: 100%;" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100"></div>
  </div>
</div>

        </div>
    


"""

snapshots[
    "test_progress_component__renders_value[False-component_kwargs2] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            
<h5 class="">a</h5>
<div class="progress-w-percent">
  <strong class="progress-value">100%</strong>
  <div class="progress progress-sm">
    <div class="progress-bar" role="progressbar" style="width: 100%;" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100"></div>
  </div>
</div>

<h5 class="">b</h5>
<div class="progress-w-percent">
  <strong class="progress-value">100%</strong>
  <div class="progress progress-sm">
    <div class="progress-bar" role="progressbar" style="width: 100%;" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100"></div>
  </div>
</div>

        </div>
    


"""

snapshots[
    "test_progress_component__renders_value[True-component_kwargs0] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            

<div class="progress-w-percent">
  <strong class="progress-value">100%</strong>
  <div class="progress progress-sm">
    <div class="progress-bar" role="progressbar" style="width: 100%;" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100"></div>
  </div>
</div>

        </div>
    


"""

snapshots[
    "test_progress_component__renders_value[True-component_kwargs1] 1"
] = """



    <div hx-get="/app1/testdashboard/component/test/"
         hx-trigger="intersect once delay:1ms">
        <div class="htmx-indicator">
            Loading...
        </div>
    </div>


"""

snapshots[
    "test_progress_component__renders_value[True-component_kwargs2] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            
<h5 class="">a</h5>
<div class="progress-w-percent">
  <strong class="progress-value">100%</strong>
  <div class="progress progress-sm">
    <div class="progress-bar" role="progressbar" style="width: 100%;" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100"></div>
  </div>
</div>

<h5 class="">b</h5>
<div class="progress-w-percent">
  <strong class="progress-value">100%</strong>
  <div class="progress progress-sm">
    <div class="progress-bar" role="progressbar" style="width: 100%;" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100"></div>
  </div>
</div>

        </div>
    


"""

snapshots[
    "test_stat_component__renders_value[False-component_kwargs0] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            <div class="stat">
  
  
  <h2>100%</h2>
  <p>
    
    <span>increase</span>
  </p>
  
</div>
        </div>
    


"""

snapshots[
    "test_stat_component__renders_value[False-component_kwargs1] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            <div class="stat">
  
  
  <h2>100%</h2>
  <p>
    
    <span>increase</span>
  </p>
  
</div>
        </div>
    


"""

snapshots[
    "test_stat_component__renders_value[False-component_kwargs2] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            <div class="stat">
  
  
  <h2>100%</h2>
  <p>
    
    <span class="text-success" style="margin-right: 0.75em">
    
      <i class="mdi mdi-arrow-up-bold"></i>
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



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            <div class="stat">
  
  
  <h2>100%</h2>
  <p>
    
    <span>increase</span>
  </p>
  
</div>
        </div>
    


"""

snapshots[
    "test_stat_component__renders_value[True-component_kwargs1] 1"
] = """



    <div hx-get="/app1/testdashboard/component/test/"
         hx-trigger="intersect once delay:1ms">
        <div class="htmx-indicator">
            Loading...
        </div>
    </div>


"""

snapshots[
    "test_stat_component__renders_value[True-component_kwargs2] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            <div class="stat">
  
  
  <h2>100%</h2>
  <p>
    
    <span class="text-success" style="margin-right: 0.75em">
    
      <i class="mdi mdi-arrow-up-bold"></i>
       Change
    </span>
    
    <span>increase</span>
  </p>
  
</div>
        </div>
    


"""

snapshots[
    "test_timeline_component__renders_value[False-component_kwargs0] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            
        </div>
    


"""

snapshots[
    "test_timeline_component__renders_value[False-component_kwargs1] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            
        </div>
    


"""

snapshots[
    "test_timeline_component__renders_value[False-component_kwargs2] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            
        </div>
    


"""

snapshots[
    "test_timeline_component__renders_value[True-component_kwargs0] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            
        </div>
    


"""

snapshots[
    "test_timeline_component__renders_value[True-component_kwargs1] 1"
] = """



    <div hx-get="/app1/testdashboard/component/test/"
         hx-trigger="intersect once delay:1ms">
        <div class="htmx-indicator">
            Loading...
        </div>
    </div>


"""

snapshots[
    "test_timeline_component__renders_value[True-component_kwargs2] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            
        </div>
    


"""

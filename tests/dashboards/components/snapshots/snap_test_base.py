# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_render[False-component_kwargs0-Chart] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            
    <script type="module">
        var data_dashapp1testdashboardcomponenttest = value;
        Plotly.newPlot(
            'dashapp1testdashboardcomponenttest',
            data_dashapp1testdashboardcomponenttest.data,
            data_dashapp1testdashboardcomponenttest.layout,
            {
                displayModeBar: "hover",
                staticPlot: false,
                responsive: true
            },
        );
    </script>


<div id="dashapp1testdashboardcomponenttest" class=""></div>


        </div>
    


"""

snapshots[
    "test_render[False-component_kwargs0-Stat] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="stat">
  
  
  <h2 class="stat__heading"></h2>
  <p class="stat__text">
    
    <span></span>
  </p>
  
</div>
        </div>
    


"""

snapshots[
    "test_render[False-component_kwargs0-Text] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            
value

        </div>
    


"""

snapshots[
    "test_render[False-component_kwargs1-Chart] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            
    <script type="module">
        var data_dashapp1testdashboardcomponenttest = value;
        Plotly.newPlot(
            'dashapp1testdashboardcomponenttest',
            data_dashapp1testdashboardcomponenttest.data,
            data_dashapp1testdashboardcomponenttest.layout,
            {
                displayModeBar: "hover",
                staticPlot: false,
                responsive: true
            },
        );
    </script>


<div id="dashapp1testdashboardcomponenttest" class=""></div>


        </div>
    


"""

snapshots[
    "test_render[False-component_kwargs1-Stat] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="stat">
  
  
  <h2 class="stat__heading"></h2>
  <p class="stat__text">
    
    <span></span>
  </p>
  
</div>
        </div>
    


"""

snapshots[
    "test_render[False-component_kwargs1-Text] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            
value

        </div>
    


"""

snapshots[
    "test_render[False-component_kwargs2-Chart] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            
    <script type="module">
        var data_dashapp1testdashboardcomponenttest = value;
        Plotly.newPlot(
            'dashapp1testdashboardcomponenttest',
            data_dashapp1testdashboardcomponenttest.data,
            data_dashapp1testdashboardcomponenttest.layout,
            {
                displayModeBar: "hover",
                staticPlot: false,
                responsive: true
            },
        );
    </script>


<div id="dashapp1testdashboardcomponenttest" class="[&#x27;a&#x27;, &#x27;b&#x27;]"></div>


        </div>
    


"""

snapshots[
    "test_render[False-component_kwargs2-Stat] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="">
  
  
  <h2 class=""></h2>
  <p class="">
    
    <span></span>
  </p>
  
</div>
        </div>
    


"""

snapshots[
    "test_render[False-component_kwargs2-Text] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            
value

        </div>
    


"""

snapshots[
    "test_render[True-component_kwargs0-Chart] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            
    <script type="module">
        var data_dashapp1testdashboardcomponenttest = value;
        Plotly.newPlot(
            'dashapp1testdashboardcomponenttest',
            data_dashapp1testdashboardcomponenttest.data,
            data_dashapp1testdashboardcomponenttest.layout,
            {
                displayModeBar: "hover",
                staticPlot: false,
                responsive: true
            },
        );
    </script>


<div id="dashapp1testdashboardcomponenttest" class=""></div>


        </div>
    


"""

snapshots[
    "test_render[True-component_kwargs0-Stat] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="stat">
  
  
  <h2 class="stat__heading"></h2>
  <p class="stat__text">
    
    <span></span>
  </p>
  
</div>
        </div>
    


"""

snapshots[
    "test_render[True-component_kwargs0-Text] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            
value

        </div>
    


"""

snapshots[
    "test_render[True-component_kwargs1-Chart] 1"
] = """



    <div hx-get="/dash/app1/testdashboard/@component/test/"
         hx-trigger="intersect once delay:1ms">
        <div class="htmx-indicator">
            Loading...
        </div>
    </div>


"""

snapshots[
    "test_render[True-component_kwargs1-Stat] 1"
] = """



    <div hx-get="/dash/app1/testdashboard/@component/test/"
         hx-trigger="intersect once delay:1ms">
        <div class="htmx-indicator">
            Loading...
        </div>
    </div>


"""

snapshots[
    "test_render[True-component_kwargs1-Text] 1"
] = """



    <div hx-get="/dash/app1/testdashboard/@component/test/"
         hx-trigger="intersect once delay:1ms">
        <div class="htmx-indicator">
            Loading...
        </div>
    </div>


"""

snapshots[
    "test_render[True-component_kwargs2-Chart] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            
    <script type="module">
        var data_dashapp1testdashboardcomponenttest = value;
        Plotly.newPlot(
            'dashapp1testdashboardcomponenttest',
            data_dashapp1testdashboardcomponenttest.data,
            data_dashapp1testdashboardcomponenttest.layout,
            {
                displayModeBar: "hover",
                staticPlot: false,
                responsive: true
            },
        );
    </script>


<div id="dashapp1testdashboardcomponenttest" class="[&#x27;a&#x27;, &#x27;b&#x27;]"></div>


        </div>
    


"""

snapshots[
    "test_render[True-component_kwargs2-Stat] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="">
  
  
  <h2 class=""></h2>
  <p class="">
    
    <span></span>
  </p>
  
</div>
        </div>
    


"""

snapshots[
    "test_render[True-component_kwargs2-Text] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            
value

        </div>
    


"""

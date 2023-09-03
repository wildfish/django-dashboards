# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_gauge_component__renders_value[False] 1"
] = """


    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="gauge">

    
    
    <script type="module">
        var componentGauge = Gauge(document.getElementById("dashapp1testdashboardcomponenttest"), {
            max: 100,
            
            value: 50,
            showValue: false,
        });

        componentGauge.setValue(0);
        componentGauge.setValueAnimated(50, 2);
    </script>

    <h2 class="gaugue-title-text"></h2>
    <div id="dashapp1testdashboardcomponenttest" class="gauge-container">
        <div class="gauge-content">
            <span class="gauge-value-text">50</span>
            
        </div>
    </div>
    
</div>
        </div>
    


"""

snapshots[
    "test_gauge_component__renders_value[True] 1"
] = """


    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="gauge">

    
    
    <script type="module">
        var componentGauge = Gauge(document.getElementById("dashapp1testdashboardcomponenttest"), {
            max: 100,
            
            value: 50,
            showValue: false,
        });

        componentGauge.setValue(0);
        componentGauge.setValueAnimated(50, 2);
    </script>

    <h2 class="gaugue-title-text"></h2>
    <div id="dashapp1testdashboardcomponenttest" class="gauge-container">
        <div class="gauge-content">
            <span class="gauge-value-text">50</span>
            
        </div>
    </div>
    
</div>
        </div>
    


"""

snapshots[
    "test_stat_component__renders_value[False-component_kwargs0] 1"
] = """


    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="gauge">

    
    
    <script type="module">
        var componentGauge = Gauge(document.getElementById("dashapp1testdashboardcomponenttest"), {
            max: 100,
            
            value: 50,
            showValue: false,
        });

        componentGauge.setValue(0);
        componentGauge.setValueAnimated(50, 2);
    </script>

    <h2 class="gaugue-title-text"></h2>
    <div id="dashapp1testdashboardcomponenttest" class="gauge-container">
        <div class="gauge-content">
            <span class="gauge-value-text">50</span>
            
        </div>
    </div>
    
</div>
        </div>
    


"""

snapshots[
    "test_stat_component__renders_value[False-component_kwargs1] 1"
] = """


    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="gauge">

    
    
    <script type="module">
        var componentGauge = Gauge(document.getElementById("dashapp1testdashboardcomponenttest"), {
            max: 100,
            
            value: 50,
            showValue: false,
        });

        componentGauge.setValue(0);
        componentGauge.setValueAnimated(50, 2);
    </script>

    <h2 class="gaugue-title-text"></h2>
    <div id="dashapp1testdashboardcomponenttest" class="gauge-container">
        <div class="gauge-content">
            <span class="gauge-value-text">50</span>
            
        </div>
    </div>
    
</div>
        </div>
    


"""

snapshots[
    "test_stat_component__renders_value[False-component_kwargs2] 1"
] = """


    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="gauge">

    
    
    <script type="module">
        var componentGauge = Gauge(document.getElementById("dashapp1testdashboardcomponenttest"), {
            max: 100,
            min: -100
            value: 50,
            showValue: false,
        });

        componentGauge.setValue(0);
        componentGauge.setValueAnimated(50, 2);
    </script>

    <h2 class="gaugue-title-text"></h2>
    <div id="dashapp1testdashboardcomponenttest" class="gauge-container">
        <div class="gauge-content">
            <span class="gauge-value-text">50</span>
            
        </div>
    </div>
    
</div>
        </div>
    


"""

snapshots[
    "test_stat_component__renders_value[False-component_kwargs3] 1"
] = """


    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="gauge">

    
    
    <script type="module">
        var componentGauge = Gauge(document.getElementById("dashapp1testdashboardcomponenttest"), {
            max: 100,
            
            value: 50,
            showValue: false,
        });

        componentGauge.setValue(0);
        componentGauge.setValueAnimated(50, 2);
    </script>

    <h2 class="gaugue-title-text"></h2>
    <div id="dashapp1testdashboardcomponenttest" class="gauge-container">
        <div class="gauge-content">
            <span class="gauge-value-text">50</span>
            <span class="gauge-sub-text">foo</span>
        </div>
    </div>
    
</div>
        </div>
    


"""

snapshots[
    "test_stat_component__renders_value[False-component_kwargs4] 1"
] = """


    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="gauge">

    
    
    <script type="module">
        var componentGauge = Gauge(document.getElementById("dashapp1testdashboardcomponenttest"), {
            max: 100,
            
            value: 50,
            showValue: false,
        });

        componentGauge.setValue(0);
        componentGauge.setValueAnimated(50, 2);
    </script>

    <h2 class="gaugue-title-text"></h2>
    <div id="dashapp1testdashboardcomponenttest" class="gauge-container">
        <div class="gauge-content">
            <span class="gauge-value-text">bar</span>
            
        </div>
    </div>
    
</div>
        </div>
    


"""

snapshots[
    "test_stat_component__renders_value[True-component_kwargs0] 1"
] = """


    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="gauge">

    
    
    <script type="module">
        var componentGauge = Gauge(document.getElementById("dashapp1testdashboardcomponenttest"), {
            max: 100,
            
            value: 50,
            showValue: false,
        });

        componentGauge.setValue(0);
        componentGauge.setValueAnimated(50, 2);
    </script>

    <h2 class="gaugue-title-text"></h2>
    <div id="dashapp1testdashboardcomponenttest" class="gauge-container">
        <div class="gauge-content">
            <span class="gauge-value-text">50</span>
            
        </div>
    </div>
    
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
            <div class="gauge">

    
    
    <script type="module">
        var componentGauge = Gauge(document.getElementById("dashapp1testdashboardcomponenttest"), {
            max: 100,
            min: -100
            value: 50,
            showValue: false,
        });

        componentGauge.setValue(0);
        componentGauge.setValueAnimated(50, 2);
    </script>

    <h2 class="gaugue-title-text"></h2>
    <div id="dashapp1testdashboardcomponenttest" class="gauge-container">
        <div class="gauge-content">
            <span class="gauge-value-text">50</span>
            
        </div>
    </div>
    
</div>
        </div>
    


"""

snapshots[
    "test_stat_component__renders_value[True-component_kwargs3] 1"
] = """


    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="gauge">

    
    
    <script type="module">
        var componentGauge = Gauge(document.getElementById("dashapp1testdashboardcomponenttest"), {
            max: 100,
            
            value: 50,
            showValue: false,
        });

        componentGauge.setValue(0);
        componentGauge.setValueAnimated(50, 2);
    </script>

    <h2 class="gaugue-title-text"></h2>
    <div id="dashapp1testdashboardcomponenttest" class="gauge-container">
        <div class="gauge-content">
            <span class="gauge-value-text">50</span>
            <span class="gauge-sub-text">foo</span>
        </div>
    </div>
    
</div>
        </div>
    


"""

snapshots[
    "test_stat_component__renders_value[True-component_kwargs4] 1"
] = """


    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div class="gauge">

    
    
    <script type="module">
        var componentGauge = Gauge(document.getElementById("dashapp1testdashboardcomponenttest"), {
            max: 100,
            
            value: 50,
            showValue: false,
        });

        componentGauge.setValue(0);
        componentGauge.setValueAnimated(50, 2);
    </script>

    <h2 class="gaugue-title-text"></h2>
    <div id="dashapp1testdashboardcomponenttest" class="gauge-container">
        <div class="gauge-content">
            <span class="gauge-value-text">bar</span>
            
        </div>
    </div>
    
</div>
        </div>
    


"""

# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_component__renders_value[False-component_kwargs0-Chart] 1"
] = """
    


    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        
    <script id="data_test" type="application/json">"value"</script>
    <script>
        /* Temp - In Sandvik plots are always called rather then passed, but maybe these will work like this, needs some through. */
        var data_test = JSON.parse(document.getElementById('data_test').textContent);
        Plotly.newPlot(
            'component-chart-test',
            data_test.data,
            data_test.layout,
        );
    </script>


<div id="component-chart-test"></div>


    </div>
    
"""

snapshots[
    "test_component__renders_value[False-component_kwargs0-HTML] 1"
] = """
    


    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        value

    </div>
    
"""

snapshots[
    "test_component__renders_value[False-component_kwargs0-Table] 1"
] = """
    


    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div id="component-table-test"></div>


    
        <script id="data_test" type="application/json">"value"</script>
    
    <script>
        
        const data_test = JSON.parse(document.getElementById('data_test').textContent);
        const rows_test = data_test.rows;
        

        /*
        TODO for more control, the data provided to the component could be
        {"data:..., "options":...} and we pass options like autoColumns down as per Sandvik
        */
        const table_test = new Tabulator("#component-table-test", {
            
            "data": rows_test,
            
            "pagination": true,
            "autoColumns": true,
            "layout": "fitColumns",
            "paginationSize": 10,
        });
    </script>




    </div>
    
"""

snapshots[
    "test_component__renders_value[False-component_kwargs0-Text] 1"
] = """
    


    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        value

    </div>
    
"""

snapshots[
    "test_component__renders_value[False-component_kwargs1-Chart] 1"
] = """
    


    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        
    <script id="data_test" type="application/json">"value"</script>
    <script>
        /* Temp - In Sandvik plots are always called rather then passed, but maybe these will work like this, needs some through. */
        var data_test = JSON.parse(document.getElementById('data_test').textContent);
        Plotly.newPlot(
            'component-chart-test',
            data_test.data,
            data_test.layout,
        );
    </script>


<div id="component-chart-test"></div>


    </div>
    
"""

snapshots[
    "test_component__renders_value[False-component_kwargs1-HTML] 1"
] = """
    


    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        value

    </div>
    
"""

snapshots[
    "test_component__renders_value[False-component_kwargs1-Table] 1"
] = """
    


    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div id="component-table-test"></div>


    
    <script>
        

        /*
        TODO for more control, the data provided to the component could be
        {"data:..., "options":...} and we pass options like autoColumns down as per Sandvik
        */
        const table_test = new Tabulator("#component-table-test", {
            
            "sortMode": "remote",
            "ajaxURL":"/None/test/?key=test",
            "paginationMode": "remote",
            "ajaxResponse": function(url, params, response){
                return {"data": response.rows, "last_page": response.last_page};
            },
            
            "pagination": true,
            "autoColumns": true,
            "layout": "fitColumns",
            "paginationSize": 10,
        });
    </script>




    </div>
    
"""

snapshots[
    "test_component__renders_value[False-component_kwargs1-Text] 1"
] = """
    


    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        value

    </div>
    
"""

snapshots[
    "test_component__renders_value[True-component_kwargs0-Chart] 1"
] = """
    


    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        
    <script id="data_test" type="application/json">"value"</script>
    <script>
        /* Temp - In Sandvik plots are always called rather then passed, but maybe these will work like this, needs some through. */
        var data_test = JSON.parse(document.getElementById('data_test').textContent);
        Plotly.newPlot(
            'component-chart-test',
            data_test.data,
            data_test.layout,
        );
    </script>


<div id="component-chart-test"></div>


    </div>
    
"""

snapshots[
    "test_component__renders_value[True-component_kwargs0-HTML] 1"
] = """
    


    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        value

    </div>
    
"""

snapshots[
    "test_component__renders_value[True-component_kwargs0-Table] 1"
] = """
    


    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div id="component-table-test"></div>


    
        <script id="data_test" type="application/json">"value"</script>
    
    <script>
        
        const data_test = JSON.parse(document.getElementById('data_test').textContent);
        const rows_test = data_test.rows;
        

        /*
        TODO for more control, the data provided to the component could be
        {"data:..., "options":...} and we pass options like autoColumns down as per Sandvik
        */
        const table_test = new Tabulator("#component-table-test", {
            
            "data": rows_test,
            
            "pagination": true,
            "autoColumns": true,
            "layout": "fitColumns",
            "paginationSize": 10,
        });
    </script>




    </div>
    
"""

snapshots[
    "test_component__renders_value[True-component_kwargs0-Text] 1"
] = """
    


    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        value

    </div>
    
"""

snapshots[
    "test_component__renders_value[True-component_kwargs1-Chart] 1"
] = """
    <div hx-get="/None/test/?key=test" hx-trigger="load"></div>
"""

snapshots[
    "test_component__renders_value[True-component_kwargs1-HTML] 1"
] = """
    <div hx-get="/None/test/?key=test" hx-trigger="load"></div>
"""

snapshots[
    "test_component__renders_value[True-component_kwargs1-Table] 1"
] = """
    <div hx-get="/None/test/?key=test" hx-trigger="load"></div>
"""

snapshots[
    "test_component__renders_value[True-component_kwargs1-Text] 1"
] = """
    <div hx-get="/None/test/?key=test" hx-trigger="load"></div>
"""

snapshots[
    "test_component__renders_value__stat[False-component_kwargs0] 1"
] = """
    


    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <h2>100%</h2>
<small>increase</small>

    </div>
    
"""

snapshots[
    "test_component__renders_value__stat[False-component_kwargs1] 1"
] = """
    


    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <h2>100%</h2>
<small>increase</small>

    </div>
    
"""

snapshots[
    "test_component__renders_value__stat[True-component_kwargs0] 1"
] = """
    


    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <h2>100%</h2>
<small>increase</small>

    </div>
    
"""

snapshots[
    "test_component__renders_value__stat[True-component_kwargs1] 1"
] = """
    <div hx-get="/None/test/?key=test" hx-trigger="load"></div>
"""

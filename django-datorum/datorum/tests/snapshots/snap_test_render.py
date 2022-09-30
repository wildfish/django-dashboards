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
        var data_test = JSON.parse(document.getElementById('data_test').textContent);
        Plotly.newPlot(
            'test',
            data_test.data,
            data_test.layout,
        );
    </script>


<div id="test"></div>


    </div>
"""

snapshots[
    "test_component__renders_value[False-component_kwargs0-Table] 1"
] = """
    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div id="test"></div>


    
        <script id="data_test" type="application/json">"value"</script>
    
    <script>
        
        let data_test = JSON.parse(document.getElementById('data_test').textContent);
        let rows_test = data_test.rows;
        

        /*
        TODO for more control, the data provided to the component could be
        */
        let table_test = new Tabulator("#test", {
            
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
        var data_test = JSON.parse(document.getElementById('data_test').textContent);
        Plotly.newPlot(
            'test',
            data_test.data,
            data_test.layout,
        );
    </script>


<div id="test"></div>


    </div>
"""

snapshots[
    "test_component__renders_value[False-component_kwargs1-Table] 1"
] = """
    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div id="test"></div>


    
    <script>
        

        /*
        TODO for more control, the data provided to the component could be
        */
        let table_test = new Tabulator("#test", {
            
            "sortMode": "remote",
            "ajaxURL":"/app1/DashboardType/component/test/?key=test",
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
    "test_component__renders_value[False-component_kwargs2-Chart] 1"
] = """
    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        
    <script id="data_test" type="application/json">"value"</script>
    <script>
        var data_test = JSON.parse(document.getElementById('data_test').textContent);
        Plotly.newPlot(
            'test',
            data_test.data,
            data_test.layout,
        );
    </script>


<div id="test"></div>


    </div>
"""

snapshots[
    "test_component__renders_value[False-component_kwargs2-Table] 1"
] = """
    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div id="test"></div>


    
        <script id="data_test" type="application/json">"value"</script>
    
    <script>
        
        let data_test = JSON.parse(document.getElementById('data_test').textContent);
        let rows_test = data_test.rows;
        

        /*
        TODO for more control, the data provided to the component could be
        */
        let table_test = new Tabulator("#test", {
            
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
    "test_component__renders_value[False-component_kwargs2-Text] 1"
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
        var data_test = JSON.parse(document.getElementById('data_test').textContent);
        Plotly.newPlot(
            'test',
            data_test.data,
            data_test.layout,
        );
    </script>


<div id="test"></div>


    </div>
"""

snapshots[
    "test_component__renders_value[True-component_kwargs0-Table] 1"
] = """
    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div id="test"></div>


    
        <script id="data_test" type="application/json">"value"</script>
    
    <script>
        
        let data_test = JSON.parse(document.getElementById('data_test').textContent);
        let rows_test = data_test.rows;
        

        /*
        TODO for more control, the data provided to the component could be
        */
        let table_test = new Tabulator("#test", {
            
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
    <div hx-get="/app1/DashboardType/component/test/" hx-trigger="intersect once, every 10s"></div>
"""

snapshots[
    "test_component__renders_value[True-component_kwargs1-Table] 1"
] = """
    <div hx-get="/app1/DashboardType/component/test/" hx-trigger="intersect once, every 10s"></div>
"""

snapshots[
    "test_component__renders_value[True-component_kwargs1-Text] 1"
] = """
    <div hx-get="/app1/DashboardType/component/test/" hx-trigger="intersect once, every 10s"></div>
"""

snapshots[
    "test_component__renders_value[True-component_kwargs2-Chart] 1"
] = """
    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        
    <script id="data_test" type="application/json">"value"</script>
    <script>
        var data_test = JSON.parse(document.getElementById('data_test').textContent);
        Plotly.newPlot(
            'test',
            data_test.data,
            data_test.layout,
        );
    </script>


<div id="test"></div>


    </div>
"""

snapshots[
    "test_component__renders_value[True-component_kwargs2-Table] 1"
] = """
    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div id="test"></div>


    
        <script id="data_test" type="application/json">"value"</script>
    
    <script>
        
        let data_test = JSON.parse(document.getElementById('data_test').textContent);
        let rows_test = data_test.rows;
        

        /*
        TODO for more control, the data provided to the component could be
        */
        let table_test = new Tabulator("#test", {
            
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
    "test_component__renders_value[True-component_kwargs2-Text] 1"
] = """
    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        
value

    </div>
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
    <div hx-get="/app1/DashboardType/component/test/" hx-trigger="intersect once, every 10s"></div>
"""

snapshots[
    "test_cta_component__renders_value[False] 1"
] = """
    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <a href="/" class="dashboard-component-cta">
  click here
</a>

    </div>
"""

snapshots[
    "test_cta_component__renders_value[True] 1"
] = """
    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <a href="/" class="dashboard-component-cta">
  click here
</a>

    </div>
"""

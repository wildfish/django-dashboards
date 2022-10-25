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
            {displayModeBar: "hover", staticPlot: false},
        );
    </script>


<div id="test"></div>


    </div>
"""

snapshots[
    "test_component__renders_value[False-component_kwargs0-Table] 1"
] = """



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div id="test">
  <table id="test_table" class="table table-striped nowrap None" style="width:100%"></table>
</div>


  
    <script id="data_test" type="application/json">"value"</script>
  
  <script id="columns_test" type="application/json">null</script>
  <script>
      var columns_test = JSON.parse(document.getElementById('columns_test').textContent);

      
          let data_test = JSON.parse(document.getElementById('data_test').textContent);
          let rows_test = data_test.data;

          var options = {
              data: rows_test,
              columns: columns_test,
              pageLength: 10,
              scrollX: true,
              searching: true,
              paging: true,
              info: true,
              ordering: true,
          }

      

      var table_test = $('#test_table').DataTable(options);
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
            {displayModeBar: "hover", staticPlot: false},
        );
    </script>


<div id="test"></div>


    </div>
"""

snapshots[
    "test_component__renders_value[False-component_kwargs1-Table] 1"
] = """



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div id="test">
  <table id="test_table" class="table table-striped nowrap None" style="width:100%"></table>
</div>


  
  <script id="columns_test" type="application/json">null</script>
  <script>
      var columns_test = JSON.parse(document.getElementById('columns_test').textContent);

      
          var options = {
              destroy: true,
              scrollX: true,
              processing: true,
              serverSide: true,
              searching: true,
              paging: true,
              info: true,
              ordering: true,
              columns: columns_test,
              pageLength: 10,
              ajax: {
                  url: "/app1/testdashboard/component/test/",
                  contentType: "application/json",
              }
          }
      

      var table_test = $('#test_table').DataTable(options);
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
            {displayModeBar: "hover", staticPlot: false},
        );
    </script>


<div id="test"></div>


    </div>
"""

snapshots[
    "test_component__renders_value[False-component_kwargs2-Table] 1"
] = """



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div id="test">
  <table id="test_table" class="table table-striped nowrap [&#x27;a&#x27;, &#x27;b&#x27;]" style="width:100%"></table>
</div>


  
    <script id="data_test" type="application/json">"value"</script>
  
  <script id="columns_test" type="application/json">null</script>
  <script>
      var columns_test = JSON.parse(document.getElementById('columns_test').textContent);

      
          let data_test = JSON.parse(document.getElementById('data_test').textContent);
          let rows_test = data_test.data;

          var options = {
              data: rows_test,
              columns: columns_test,
              pageLength: 10,
              scrollX: true,
              searching: true,
              paging: true,
              info: true,
              ordering: true,
          }

      

      var table_test = $('#test_table').DataTable(options);
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
            {displayModeBar: "hover", staticPlot: false},
        );
    </script>


<div id="test"></div>


    </div>
"""

snapshots[
    "test_component__renders_value[True-component_kwargs0-Table] 1"
] = """



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div id="test">
  <table id="test_table" class="table table-striped nowrap None" style="width:100%"></table>
</div>


  
    <script id="data_test" type="application/json">"value"</script>
  
  <script id="columns_test" type="application/json">null</script>
  <script>
      var columns_test = JSON.parse(document.getElementById('columns_test').textContent);

      
          let data_test = JSON.parse(document.getElementById('data_test').textContent);
          let rows_test = data_test.data;

          var options = {
              data: rows_test,
              columns: columns_test,
              pageLength: 10,
              scrollX: true,
              searching: true,
              paging: true,
              info: true,
              ordering: true,
          }

      

      var table_test = $('#test_table').DataTable(options);
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



    <div hx-get="/app1/testdashboard/component/test/"
         hx-trigger="intersect once delay:199ms"></div>
"""

snapshots[
    "test_component__renders_value[True-component_kwargs1-Table] 1"
] = """



    <div hx-get="/app1/testdashboard/component/test/"
         hx-trigger="intersect once delay:52ms"></div>
"""

snapshots[
    "test_component__renders_value[True-component_kwargs1-Text] 1"
] = """



    <div hx-get="/app1/testdashboard/component/test/"
         hx-trigger="intersect once delay:55ms"></div>
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
            {displayModeBar: "hover", staticPlot: false},
        );
    </script>


<div id="test"></div>


    </div>
"""

snapshots[
    "test_component__renders_value[True-component_kwargs2-Table] 1"
] = """



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div id="test">
  <table id="test_table" class="table table-striped nowrap [&#x27;a&#x27;, &#x27;b&#x27;]" style="width:100%"></table>
</div>


  
    <script id="data_test" type="application/json">"value"</script>
  
  <script id="columns_test" type="application/json">null</script>
  <script>
      var columns_test = JSON.parse(document.getElementById('columns_test').textContent);

      
          let data_test = JSON.parse(document.getElementById('data_test').textContent);
          let rows_test = data_test.data;

          var options = {
              data: rows_test,
              columns: columns_test,
              pageLength: 10,
              scrollX: true,
              searching: true,
              paging: true,
              info: true,
              ordering: true,
          }

      

      var table_test = $('#test_table').DataTable(options);
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
        <div class="stat">
  
  
  <h2>100%</h2>
  <p>
    
    <span>increase</span>
  </p>
  
</div>
    </div>
"""

snapshots[
    "test_component__renders_value__stat[False-component_kwargs1] 1"
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
    "test_component__renders_value__stat[True-component_kwargs0] 1"
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
    "test_component__renders_value__stat[True-component_kwargs1] 1"
] = """



    <div hx-get="/app1/testdashboard/component/test/"
         hx-trigger="intersect once delay:131ms"></div>
"""

snapshots[
    "test_cta_component__renders_value[False] 1"
] = """



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <a href="/" class="None">
  click here
</a>

    </div>
"""

snapshots[
    "test_cta_component__renders_value[True] 1"
] = """



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <a href="/" class="None">
  click here
</a>

    </div>
"""

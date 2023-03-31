# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_render[False-component_kwargs0-BasicTable] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            

<div id="test">
  <table id="test_table" class="table" style="width:100%">
    <thead>
    
    </thead>
    <tbody>
    
    </tbody>
  </table>
</div>

        </div>
    


"""

snapshots[
    "test_render[False-component_kwargs0-Table] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            <div id="test">
  <table id="test_table" class="table" style="width:100%"></table>
</div>


  
    <script id="data_test" type="application/json">"value"</script>
  
  <script id="columns_test" type="application/json">""</script>
  <script type="module">
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
    "test_render[False-component_kwargs1-BasicTable] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            

<div id="test">
  <table id="test_table" class="table" style="width:100%">
    <thead>
    
    </thead>
    <tbody>
    
    </tbody>
  </table>
</div>

        </div>
    


"""

snapshots[
    "test_render[False-component_kwargs1-Table] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            <div id="test">
  <table id="test_table" class="table" style="width:100%"></table>
</div>


  
  <script id="columns_test" type="application/json">""</script>
  <script type="module">
      var columns_test = JSON.parse(document.getElementById('columns_test').textContent);

      
          $.ajaxSetup({
             headers: { "X-CSRFToken": JSON.parse(document.body.getAttribute("hx-headers"))["X-CSRFToken"]}
          });
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
                  url: "/dash/app1/testdashboard/@component/test/",
                  type: "POST",
                  dataFilter: function(data){
                    let json = jQuery.parseJSON( data );
                    json.recordsTotal = json.total;
                    json.recordsFiltered = json.filtered;
                    return JSON.stringify( json );
                }
              }
          }
      

      var table_test = $('#test_table').DataTable(options);
  </script>




        </div>
    


"""

snapshots[
    "test_render[False-component_kwargs2-BasicTable] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            

<div id="test">
  <table id="test_table" class="table" style="width:100%">
    <thead>
    
    </thead>
    <tbody>
    
    </tbody>
  </table>
</div>

        </div>
    


"""

snapshots[
    "test_render[False-component_kwargs2-Table] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            <div id="test">
  <table id="test_table" class="table" style="width:100%"></table>
</div>


  
    <script id="data_test" type="application/json">"value"</script>
  
  <script id="columns_test" type="application/json">""</script>
  <script type="module">
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
    "test_render[True-component_kwargs0-BasicTable] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            

<div id="test">
  <table id="test_table" class="table" style="width:100%">
    <thead>
    
    </thead>
    <tbody>
    
    </tbody>
  </table>
</div>

        </div>
    


"""

snapshots[
    "test_render[True-component_kwargs0-Table] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            <div id="test">
  <table id="test_table" class="table" style="width:100%"></table>
</div>


  
    <script id="data_test" type="application/json">"value"</script>
  
  <script id="columns_test" type="application/json">""</script>
  <script type="module">
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
    "test_render[True-component_kwargs1-BasicTable] 1"
] = """



    <div hx-get="/dash/app1/testdashboard/@component/test/"
         hx-trigger="intersect once delay:1ms">
        <div class="htmx-indicator">
            Loading...
        </div>
    </div>


"""

snapshots[
    "test_render[True-component_kwargs1-Table] 1"
] = """



    <div hx-get="/dash/app1/testdashboard/@component/test/"
         hx-trigger="intersect once delay:1ms">
        <div class="htmx-indicator">
            Loading...
        </div>
    </div>


"""

snapshots[
    "test_render[True-component_kwargs2-BasicTable] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            

<div id="test">
  <table id="test_table" class="table" style="width:100%">
    <thead>
    
    </thead>
    <tbody>
    
    </tbody>
  </table>
</div>

        </div>
    


"""

snapshots[
    "test_render[True-component_kwargs2-Table] 1"
] = """



    
        <div id="component-test-inner" class="dashboard-component-inner fade-in">
            <div id="test">
  <table id="test_table" class="table" style="width:100%"></table>
</div>


  
    <script id="data_test" type="application/json">"value"</script>
  
  <script id="columns_test" type="application/json">""</script>
  <script type="module">
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

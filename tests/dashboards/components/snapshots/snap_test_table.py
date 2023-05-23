# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_render[False-component_kwargs0-BasicTable] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            

<div id="dashapp1testdashboardcomponenttest">
  <table id="dashapp1testdashboardcomponenttest_table" class="table" style="width:100%">
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



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div id="dashapp1testdashboardcomponenttest">
  <table id="dashapp1testdashboardcomponenttest_table" class="table" style="width:100%"></table>
</div>


  
    <script id="data_dashapp1testdashboardcomponenttest" type="application/json">"value"</script>
  
  <script id="columns_dashapp1testdashboardcomponenttest" type="application/json">""</script>
  <script id="order_dashapp1testdashboardcomponenttest" type="application/json">""</script>
  <script type="module">
      var columns_dashapp1testdashboardcomponenttest = JSON.parse(document.getElementById('columns_dashapp1testdashboardcomponenttest').textContent);
      var order_dashapp1testdashboardcomponenttest = JSON.parse(document.getElementById('order_dashapp1testdashboardcomponenttest').textContent);

      
          let data_dashapp1testdashboardcomponenttest = JSON.parse(document.getElementById('data_dashapp1testdashboardcomponenttest').textContent);
          let rows_dashapp1testdashboardcomponenttest = data_dashapp1testdashboardcomponenttest.data;

          var options = {
              data: rows_dashapp1testdashboardcomponenttest,
              columns: columns_dashapp1testdashboardcomponenttest,
              pageLength: 10,
              scrollX: true,
              searching: true,
              paging: true,
              info: true,
              ordering: true,
              order: order_dashapp1testdashboardcomponenttest,
          }

      

      var table_dashapp1testdashboardcomponenttest = $('#dashapp1testdashboardcomponenttest_table').DataTable(options);
  </script>




        </div>
    


"""

snapshots[
    "test_render[False-component_kwargs1-BasicTable] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            

<div id="dashapp1testdashboardcomponenttest">
  <table id="dashapp1testdashboardcomponenttest_table" class="table" style="width:100%">
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



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div id="dashapp1testdashboardcomponenttest">
  <table id="dashapp1testdashboardcomponenttest_table" class="table" style="width:100%"></table>
</div>


  
  <script id="columns_dashapp1testdashboardcomponenttest" type="application/json">""</script>
  <script id="order_dashapp1testdashboardcomponenttest" type="application/json">""</script>
  <script type="module">
      var columns_dashapp1testdashboardcomponenttest = JSON.parse(document.getElementById('columns_dashapp1testdashboardcomponenttest').textContent);
      var order_dashapp1testdashboardcomponenttest = JSON.parse(document.getElementById('order_dashapp1testdashboardcomponenttest').textContent);

      
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
              columns: columns_dashapp1testdashboardcomponenttest,
              pageLength: 10,
              order: order_dashapp1testdashboardcomponenttest,
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
      

      var table_dashapp1testdashboardcomponenttest = $('#dashapp1testdashboardcomponenttest_table').DataTable(options);
  </script>




        </div>
    


"""

snapshots[
    "test_render[False-component_kwargs2-BasicTable] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            

<div id="dashapp1testdashboardcomponenttest">
  <table id="dashapp1testdashboardcomponenttest_table" class="table" style="width:100%">
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



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div id="dashapp1testdashboardcomponenttest">
  <table id="dashapp1testdashboardcomponenttest_table" class="table" style="width:100%"></table>
</div>


  
    <script id="data_dashapp1testdashboardcomponenttest" type="application/json">"value"</script>
  
  <script id="columns_dashapp1testdashboardcomponenttest" type="application/json">""</script>
  <script id="order_dashapp1testdashboardcomponenttest" type="application/json">""</script>
  <script type="module">
      var columns_dashapp1testdashboardcomponenttest = JSON.parse(document.getElementById('columns_dashapp1testdashboardcomponenttest').textContent);
      var order_dashapp1testdashboardcomponenttest = JSON.parse(document.getElementById('order_dashapp1testdashboardcomponenttest').textContent);

      
          let data_dashapp1testdashboardcomponenttest = JSON.parse(document.getElementById('data_dashapp1testdashboardcomponenttest').textContent);
          let rows_dashapp1testdashboardcomponenttest = data_dashapp1testdashboardcomponenttest.data;

          var options = {
              data: rows_dashapp1testdashboardcomponenttest,
              columns: columns_dashapp1testdashboardcomponenttest,
              pageLength: 10,
              scrollX: true,
              searching: true,
              paging: true,
              info: true,
              ordering: true,
              order: order_dashapp1testdashboardcomponenttest,
          }

      

      var table_dashapp1testdashboardcomponenttest = $('#dashapp1testdashboardcomponenttest_table').DataTable(options);
  </script>




        </div>
    


"""

snapshots[
    "test_render[True-component_kwargs0-BasicTable] 1"
] = """



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            

<div id="dashapp1testdashboardcomponenttest">
  <table id="dashapp1testdashboardcomponenttest_table" class="table" style="width:100%">
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



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div id="dashapp1testdashboardcomponenttest">
  <table id="dashapp1testdashboardcomponenttest_table" class="table" style="width:100%"></table>
</div>


  
    <script id="data_dashapp1testdashboardcomponenttest" type="application/json">"value"</script>
  
  <script id="columns_dashapp1testdashboardcomponenttest" type="application/json">""</script>
  <script id="order_dashapp1testdashboardcomponenttest" type="application/json">""</script>
  <script type="module">
      var columns_dashapp1testdashboardcomponenttest = JSON.parse(document.getElementById('columns_dashapp1testdashboardcomponenttest').textContent);
      var order_dashapp1testdashboardcomponenttest = JSON.parse(document.getElementById('order_dashapp1testdashboardcomponenttest').textContent);

      
          let data_dashapp1testdashboardcomponenttest = JSON.parse(document.getElementById('data_dashapp1testdashboardcomponenttest').textContent);
          let rows_dashapp1testdashboardcomponenttest = data_dashapp1testdashboardcomponenttest.data;

          var options = {
              data: rows_dashapp1testdashboardcomponenttest,
              columns: columns_dashapp1testdashboardcomponenttest,
              pageLength: 10,
              scrollX: true,
              searching: true,
              paging: true,
              info: true,
              ordering: true,
              order: order_dashapp1testdashboardcomponenttest,
          }

      

      var table_dashapp1testdashboardcomponenttest = $('#dashapp1testdashboardcomponenttest_table').DataTable(options);
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



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            

<div id="dashapp1testdashboardcomponenttest">
  <table id="dashapp1testdashboardcomponenttest_table" class="table" style="width:100%">
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



    
        <div id="component-dashapp1testdashboardcomponenttest-inner" class="dashboard-component-inner fade-in">
            <div id="dashapp1testdashboardcomponenttest">
  <table id="dashapp1testdashboardcomponenttest_table" class="table" style="width:100%"></table>
</div>


  
    <script id="data_dashapp1testdashboardcomponenttest" type="application/json">"value"</script>
  
  <script id="columns_dashapp1testdashboardcomponenttest" type="application/json">""</script>
  <script id="order_dashapp1testdashboardcomponenttest" type="application/json">""</script>
  <script type="module">
      var columns_dashapp1testdashboardcomponenttest = JSON.parse(document.getElementById('columns_dashapp1testdashboardcomponenttest').textContent);
      var order_dashapp1testdashboardcomponenttest = JSON.parse(document.getElementById('order_dashapp1testdashboardcomponenttest').textContent);

      
          let data_dashapp1testdashboardcomponenttest = JSON.parse(document.getElementById('data_dashapp1testdashboardcomponenttest').textContent);
          let rows_dashapp1testdashboardcomponenttest = data_dashapp1testdashboardcomponenttest.data;

          var options = {
              data: rows_dashapp1testdashboardcomponenttest,
              columns: columns_dashapp1testdashboardcomponenttest,
              pageLength: 10,
              scrollX: true,
              searching: true,
              paging: true,
              info: true,
              ordering: true,
              order: order_dashapp1testdashboardcomponenttest,
          }

      

      var table_dashapp1testdashboardcomponenttest = $('#dashapp1testdashboardcomponenttest_table').DataTable(options);
  </script>




        </div>
    


"""

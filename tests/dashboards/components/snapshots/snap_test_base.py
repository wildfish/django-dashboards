# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_render[False-component_kwargs0-Chart] 1'] = '''



    
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
'''

snapshots['test_render[False-component_kwargs0-Progress] 1'] = '''



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        
    </div>
'''

snapshots['test_render[False-component_kwargs0-Stat] 1'] = '''



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div class="stat">
  
  
  <h2></h2>
  <p>
    
    <span></span>
  </p>
  
</div>
    </div>
'''

snapshots['test_render[False-component_kwargs0-Text] 1'] = '''



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        
value

    </div>
'''

snapshots['test_render[False-component_kwargs0-Timeline] 1'] = '''



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div class="None">
  
</div>
    </div>
'''

snapshots['test_render[False-component_kwargs1-Chart] 1'] = '''



    
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
'''

snapshots['test_render[False-component_kwargs1-Progress] 1'] = '''



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        
    </div>
'''

snapshots['test_render[False-component_kwargs1-Stat] 1'] = '''



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div class="stat">
  
  
  <h2></h2>
  <p>
    
    <span></span>
  </p>
  
</div>
    </div>
'''

snapshots['test_render[False-component_kwargs1-Text] 1'] = '''



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        
value

    </div>
'''

snapshots['test_render[False-component_kwargs1-Timeline] 1'] = '''



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div class="None">
  
</div>
    </div>
'''

snapshots['test_render[False-component_kwargs2-Chart] 1'] = '''



    
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
'''

snapshots['test_render[False-component_kwargs2-Progress] 1'] = '''



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        
    </div>
'''

snapshots['test_render[False-component_kwargs2-Stat] 1'] = '''



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div class="stat">
  
  
  <h2></h2>
  <p>
    
    <span></span>
  </p>
  
</div>
    </div>
'''

snapshots['test_render[False-component_kwargs2-Text] 1'] = '''



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        
value

    </div>
'''

snapshots['test_render[False-component_kwargs2-Timeline] 1'] = '''



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div class="[&#x27;a&#x27;, &#x27;b&#x27;]">
  
</div>
    </div>
'''

snapshots['test_render[True-component_kwargs0-Chart] 1'] = '''



    
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
'''

snapshots['test_render[True-component_kwargs0-Progress] 1'] = '''



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        
    </div>
'''

snapshots['test_render[True-component_kwargs0-Stat] 1'] = '''



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div class="stat">
  
  
  <h2></h2>
  <p>
    
    <span></span>
  </p>
  
</div>
    </div>
'''

snapshots['test_render[True-component_kwargs0-Text] 1'] = '''



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        
value

    </div>
'''

snapshots['test_render[True-component_kwargs0-Timeline] 1'] = '''



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div class="None">
  
</div>
    </div>
'''

snapshots['test_render[True-component_kwargs1-Chart] 1'] = '''



    <div hx-get="/app1/testdashboard/component/test/"
         hx-trigger="intersect once delay:1ms"></div>
'''

snapshots['test_render[True-component_kwargs1-Progress] 1'] = '''



    <div hx-get="/app1/testdashboard/component/test/"
         hx-trigger="intersect once delay:1ms"></div>
'''

snapshots['test_render[True-component_kwargs1-Stat] 1'] = '''



    <div hx-get="/app1/testdashboard/component/test/"
         hx-trigger="intersect once delay:1ms"></div>
'''

snapshots['test_render[True-component_kwargs1-Text] 1'] = '''



    <div hx-get="/app1/testdashboard/component/test/"
         hx-trigger="intersect once delay:1ms"></div>
'''

snapshots['test_render[True-component_kwargs1-Timeline] 1'] = '''



    <div hx-get="/app1/testdashboard/component/test/"
         hx-trigger="intersect once delay:1ms"></div>
'''

snapshots['test_render[True-component_kwargs2-Chart] 1'] = '''



    
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
'''

snapshots['test_render[True-component_kwargs2-Progress] 1'] = '''



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        
    </div>
'''

snapshots['test_render[True-component_kwargs2-Stat] 1'] = '''



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div class="stat">
  
  
  <h2></h2>
  <p>
    
    <span></span>
  </p>
  
</div>
    </div>
'''

snapshots['test_render[True-component_kwargs2-Text] 1'] = '''



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        
value

    </div>
'''

snapshots['test_render[True-component_kwargs2-Timeline] 1'] = '''



    
    <div id="component-test-inner" class="dashboard-component-inner fade-in">
        <div class="[&#x27;a&#x27;, &#x27;b&#x27;]">
  
</div>
    </div>
'''

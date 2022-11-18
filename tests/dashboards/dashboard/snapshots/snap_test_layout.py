# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_dashboard__render_layout 1"
] = """}{<div class="span-12 "><hr /></div><div class="span-12 ">
  <div class="span-99 css_style">
  



    
    <div id="component-component_1-inner" class="dashboard-component-inner fade-in">
        
value

    </div>

</div><div class="span-12 css_style">
  



    <div hx-get="/app1/testdashboard/component/component_2/"
         hx-trigger="intersect once delay:1ms"></div>

</div>
</div>"""

snapshots[
    "test_header__render 1"
] = '<div class="span-12 "><h2>some text....</h2></div>'

snapshots["test_html__render 1"] = '<div class="span-12 ">some text....</div>'

snapshots[
    "test_html_component__render[Card] 1"
] = """<div class="span-6 ">
  <div class="card css_class">
    
    
    <div class="card-body">
      



    
    <div id="component-component_1-inner" class="dashboard-component-inner fade-in">
        
value

    </div>

    </div>
    
  </div>
</div>"""

snapshots[
    "test_html_component__render[Div] 1"
] = """<div class="span-12 css_class">
  



    
    <div id="component-component_1-inner" class="dashboard-component-inner fade-in">
        
value

    </div>

</div>"""

snapshots[
    "test_html_component__render[Tab] 1"
] = """<div :class="{ \'active show\': tab === \'component_1\' }" x-show="tab === \'component_1\'">
    <div class="span-6 css_class">
  
</div>
</div>"""

snapshots[
    "test_layout_component__render 1"
] = """



    
    <div id="component-component_1-inner" class="dashboard-component-inner fade-in">
        
value

    </div>




    <div hx-get="/app1/testdashboard/component/component_2/"
         hx-trigger="intersect once delay:1ms"></div>
"""

snapshots[
    "test_layout_component__unknown_component_ignored 1"
] = """



    
    <div id="component-component_1-inner" class="dashboard-component-inner fade-in">
        
value

    </div>




    <div hx-get="/app1/testdashboard/component/component_2/"
         hx-trigger="intersect once delay:1ms"></div>




    
    <div id="component-component_3-inner" class="dashboard-component-inner fade-in">
        
value from callable

    </div>
"""

snapshots[
    "test_tab_container__render 1"
] = """<div class="span-6 tab-container" x-data="{ tab: \'htmlhtmlsome-text-width12\' }">
    <ul id="" class="" >
        <li class="None">
  <a :class="{ \'active\': tab === \'htmlhtmlsome-text-width12\' }" x-on:click.prevent="tab = \'htmlhtmlsome-text-width12\'" href="#" class="None">
    HTML(html=&#x27;some text....&#x27;, width=12)
  </a>
</li>
    </ul>

    <div class="tab-content">
        <div :class="{ \'active show\': tab === \'htmlhtmlsome-text-width12\' }" x-show="tab === \'htmlhtmlsome-text-width12\'">
    <div class="span-6 tab-content">
  
</div>
</div>
    </div>
</div>"""

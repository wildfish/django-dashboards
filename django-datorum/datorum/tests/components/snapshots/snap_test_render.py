# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_text__deferred_value_not_shown 1"
] = """
        
        
    


    
    <div id="component-None-inner" class="fade-in">
        value

    </div>


    """

snapshots[
    "test_text__deferred_value_shown 1"
] = """
        
        
    


    
    <div id="component-None-inner" class="fade-in">
        value

    </div>


    """

snapshots[
    "test_text__renders_deferred_value 1"
] = """
        
        
    


    
    <div id="component-None-inner" class="fade-in">
        value

    </div>


    """

snapshots[
    "test_text__renders_value 1"
] = """
        
        
    


    
    <div id="component-None-inner" class="fade-in">
        value

    </div>


    """

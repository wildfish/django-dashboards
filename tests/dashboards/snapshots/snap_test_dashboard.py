# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots["test__get_attributes_order 1"] = GenericRepr(
    "dict_keys(['component_1', 'component_2', 'component_3'])"
)

snapshots["test__get_attributes_order__with_parent 1"] = GenericRepr(
    "dict_keys(['component_1', 'component_2', 'component_3', 'component_4', 'component_5', 'component_6', 'component_7'])"
)

snapshots["test_dashboard__get_context 1"] = {
    "components": [
        GenericRepr(
            "Text(template_name=None, value='value', defer=None, defer_url=None, dependents=None, key='component_1', dashboard=<class 'tests.dashboards.dashboards.TestDashboard'>, render_type='Text', serializable=True, icon=None, css_classes=None, width=6, poll_rate=None, trigger_on=None, dependent_components=None, template='wildcoeus/dashboards/components/text/text.html', mark_safe=False)"
        ),
        GenericRepr(
            "Text(template_name=None, value=None, defer=<function TestDashboard.<lambda> at 0x10570a5e0>, defer_url=None, dependents=None, key='component_2', dashboard=<class 'tests.dashboards.dashboards.TestDashboard'>, render_type='Text', serializable=True, icon=None, css_classes=None, width=6, poll_rate=None, trigger_on=None, dependent_components=None, template='wildcoeus/dashboards/components/text/text.html', mark_safe=False)"
        ),
        GenericRepr(
            "Text(template_name=None, value=<function TestDashboard.<lambda> at 0x105715670>, defer=None, defer_url=None, dependents=None, key='component_3', dashboard=<class 'tests.dashboards.dashboards.TestDashboard'>, render_type='Text', serializable=True, icon=None, css_classes=None, width=6, poll_rate=None, trigger_on=None, dependent_components=None, template='wildcoeus/dashboards/components/text/text.html', mark_safe=False)"
        ),
    ],
    "dashboard": GenericRepr(
        "<tests.dashboards.dashboards.TestDashboard object at 0x100000000>"
    ),
}

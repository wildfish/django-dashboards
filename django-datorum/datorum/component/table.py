from dataclasses import dataclass

from .base import Component


@dataclass
class Tabulator(Component):
    """
    Basic table example, we'd also want it to handle pagination/searching/filter/ordering remotely etc.

    That should all be possible via the defer calls, I've set the table to ajax if deferred and that passes
    the params needed to sort/filter etc, we'd just need to handle that in there, we could probably write some helper
    functions maybe here like Tabulator.apply_sort(data) that we could leverage when deferring data.

    Also need a meta/options call, either part of data or part of the component (Component.Options maybe) which can
    be passed to front end for config options and setting titles of columns/widths etc.

    Atm the deferred version of this is a little confusing, if deferred, we load the component in via HTMX because
    that's what is deferred does, but then we don't render the data as ajax is called to get the data s JSON to
    leverage tabulator (and most js table libs) ajax rendering. Might be a better way to do this maybe we need a is_ajax
    also but that feels complicated, this way works for a poc.
    """

    template: str = "datorum/components/table/tabulator.html"

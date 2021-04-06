from ipywidgets.widgets.widget import widget_serialization
from traitlets import Unicode, Any
from ipyvue import VueTemplate

from .force_load import force_load

class FlatSurface(VueTemplate):
    r"""
    A Flat Surfacae.
    """
    __force = Any(force_load, read_only=True).tag(sync=True, **widget_serialization)
    template = Unicode(r"""
    <div>
        TODO
    </div>
    """).tag(sync=True)

r"""
A generic base class interfacing with the vue_flatsurf frontend widgets.
"""
# ********************************************************************
#  This file is part of ipyvue-flatsurf.
#
#        Copyright (C) 2021 Julian Rüth
#
#  ipyvue-flatsurf is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  ipyvue-flatsurf is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  ipyvue-flatsurf. If not, see <https://www.gnu.org/licenses/>.
# ********************************************************************

from ipyvue import VueTemplate
from traitlets import Unicode, Any, List
from ipywidgets.widgets.widget import widget_serialization
from ipyvue_flatsurf.force_load import force_load


class VueFlatsurfWidget(VueTemplate):
    r"""
    Generic base class for most other widgets to interface with vue-flatsurf's
    Widget component.
    """

    def __init__(self, triangulation, action="glue", flow_components=[]):
        VueTemplate.__init__(self)
        self.template = VueFlatsurfWidget._create_template(*[name[:-len('_prop')] for name in dir(type(self)) if name.endswith("_prop")])
        self.triangulation = triangulation
        self.action = action
        self.flow_components = flow_components

    @property
    def triangulation(self):
        raise NotImplementedError("cannot parse the triangulation underlying a widget yet")

    @triangulation.setter
    def triangulation(self, triangulation):
        from ipyvue_flatsurf.encoding.flat_triangulation import encode_flat_triangulation
        self.triangulation_prop = VueFlatsurfWidget._to_yaml(encode_flat_triangulation(triangulation))

    @property
    def action(self):
        return self.action_prop

    @action.setter
    def action(self, action):
        self.action_prop = action

    @property
    def flow_components(self):
        raise NotImplementedError("cannot parse the flow components displayed in a widget yet")

    @flow_components.setter
    def flow_components(self, flow_components, deformation=None):
        from ipyvue_flatsurf.encoding.flow_component import encode_flow_component
        self.flow_components_prop = [VueFlatsurfWidget._to_yaml(encode_flow_component(component, deformation)) for component in flow_components]

    @classmethod
    def _to_yaml(cls, x):
        r"""
        Return `x` as a YAML string.

        EXAMPLES::

            >>> VueFlatsurfWidget._to_yaml({"a": 1337})
            'a: 1337'

        """
        if not isinstance(x, dict):
            raise NotImplementedError("Cannot convert this object to YAML yet.")

        from io import StringIO
        buffer = StringIO()
        from ruamel.yaml import YAML
        yaml = YAML()
        yaml.dump(x, buffer)
        buffer.seek(0)
        return buffer.read().strip()

    @classmethod
    def _create_template(cls, *props):
        r"""
        Create a Vue template snippet to include the vue-flatsurf widget with
        the given props.

        EXAMPLES::

            >>> VueFlatsurfWidget._create_template("triangulation", "snake_case");
            '<vue-flatsurf-widget :triangulation="triangulation_prop" :snake-case="snake_case_prop" />'
        """
        def kebab(name): return name.replace('_', '-')
        return f"""<vue-flatsurf-widget { " ".join([f':{kebab(prop)}="{prop}_prop"' for prop in props]) } />"""

    __force = Any(force_load, read_only=True).tag(sync=True, **widget_serialization)

    template = Unicode("").tag(sync=True)
    triangulation_prop = Unicode("").tag(sync=True)
    action_prop = Any(None).tag(sync=True)
    flow_components_prop = List([]).tag(sync=True)

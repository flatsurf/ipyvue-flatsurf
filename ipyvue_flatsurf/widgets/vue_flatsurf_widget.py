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
from traitlets import Unicode, Any
from ipywidgets.widgets.widget import widget_serialization
from ipyvue_flatsurf.force_load import force_load


class VueFlatsurfWidget(VueTemplate):
    r"""
    Generic base class for most other widgets to interface with vue-flatsurf's
    Widget component.
    """

    def __init__(self, triangulation, action="glue"):
        VueTemplate.__init__(self)
        self.template = VueFlatsurfWidget._create_template("triangulation", "action")
        self.triangulation = VueFlatsurfWidget._to_yaml(VueFlatsurfWidget._encode_flat_triangulation(triangulation))
        self.action = action

    @classmethod
    def _encode_flat_triangulation(cls, triangulation):
        r"""
        Return the flat triangulation encoded as a primitive type.

        EXAMPLES::

            >>> from flatsurf import translation_surfaces, polygons, similarity_surfaces
            >>> t = polygons.triangle(1, 1, 1)
            >>> B = similarity_surfaces.billiard(t)
            >>> S = B.minimal_cover('translation')

            >>> from flatsurf.geometry.pyflatsurf_conversion import to_pyflatsurf
            >>> T = to_pyflatsurf(S)

            >>> VueFlatsurfWidget._encode_flat_triangulation(T) == {
            ...   'vertices': [[1, -3, -9, 6, -7, 4], [-1, -5, 9, -8, 7, 2], [-2, -6, 5, -4, 8, 3]],
            ...   'vectors': {
            ...      1: {'x': 1.0, 'y': 0.0},
            ...      2: {'x': -0.5, 'y': 0.8660254037844386},
            ...      3: {'x': -0.5, 'y': -0.8660254037844386},
            ...      4: {'x': 0.5, 'y': -0.8660254037844386},
            ...      5: {'x': 0.5, 'y': 0.8660254037844386},
            ...      6: {'x': -1.0, 'y': 0.0},
            ...      7: {'x': 0.5, 'y': 0.8660254037844386},
            ...      8: {'x': -1.0, 'y': 0.0},
            ...      9: {'x': 0.5, 'y': -0.8660254037844386}
            ...   }
            ... }
            True

        """
        return {
            "vertices": [list(he.id() for he in triangulation.atVertex(v)) for v in triangulation.vertices()],
            "vectors": {
                he.id(): {
                    "x": float(triangulation.fromHalfEdge(he).x()),
                    "y": float(triangulation.fromHalfEdge(he).y()),
                } for he in triangulation.halfEdges() if he.id() > 0
            }
        }

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

            >>> VueFlatsurfWidget._create_template("triangulation");
            '<vue-flatsurf-widget :triangulation="triangulation" />'
        """
        return f"""<vue-flatsurf-widget { " ".join([f':{prop}="{prop}"' for prop in props]) } />"""

    __force = Any(force_load, read_only=True).tag(sync=True, **widget_serialization)

    template = Unicode("").tag(sync=True)
    triangulation = Unicode("").tag(sync=True)
    action = Any(None).tag(sync=True)

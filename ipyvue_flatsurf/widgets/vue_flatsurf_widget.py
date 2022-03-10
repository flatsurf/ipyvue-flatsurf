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
from traitlets import Unicode, Any, List, Bool
from ipywidgets.widgets.widget import widget_serialization
from ipyvue_flatsurf.force_load import force_load
from ipyvue_async import CommWidget


class VueFlatsurfWidget(VueTemplate, CommWidget):
    r"""
    Generic base class for most other widgets to interface with vue-flatsurf's
    Widget component.
    """

    def __init__(self, triangulation, action="glue", flow_components=[]):
        super().__init__()
        self.template = VueFlatsurfWidget._create_template(*[name[:-len('_prop')] for name in dir(type(self)) if name.endswith("_prop")])
        self.triangulation = triangulation
        self.action = action
        self.flow_components = flow_components
        self.path = None
        self.saddle_connections = []

    @property
    def triangulation(self):
        r"""
        The flat triangulation visible in the widget.

        EXAMPLES::

            >>> from flatsurf import translation_surfaces
            >>> S = translation_surfaces.square_torus()

            >>> from ipyvue_flatsurf import Widget
            >>> W = Widget(S)
            >>> W.triangulation
            FlatTriangulationCombinatorial(vertices = (1, -3, 2, -1, 3, -2), faces = (1, 2, 3)(-1, -2, -3)) with vectors {1: (1, 1), 2: (-1, 0), 3: (0, -1)}

        ::

            >>> from flatsurf.geometry.pyflatsurf_conversion import to_pyflatsurf
            >>> W.triangulation = to_pyflatsurf(S)

        """
        return self._triangulation

    @triangulation.setter
    def triangulation(self, triangulation):
        self._triangulation = triangulation

        from ipyvue_flatsurf.encoding.flat_triangulation_encoding import encode_flat_triangulation
        self.triangulation_prop = VueFlatsurfWidget._to_yaml(encode_flat_triangulation(triangulation))

    @property
    def action(self):
        r"""
        The currently selected interaction with the widget, can be `None`,
        `"glue"`, or `"path"`.

        EXAMPLES::

            >>> from flatsurf import translation_surfaces
            >>> S = translation_surfaces.square_torus();

            >>> from ipyvue_flatsurf import Widget
            >>> W = Widget(S)
            >>> W.action
            'glue'

        ::

            >>> W.action = "glue"
            >>> W.action = "path"
            >>> W.action = None

        """
        return self.action_prop

    @action.setter
    def action(self, action):
        self.action_prop = action

    @property
    def flow_components(self):
        r"""
        The flow components currently visible in the widget.

        EXAMPLES::

            >>> from flatsurf import translation_surfaces, GL2ROrbitClosure
            >>> S = translation_surfaces.square_torus()
            >>> O = GL2ROrbitClosure(S)
            >>> D = next(O.decompositions(bound=64))
            >>> component = D.components()[0]

            >>> from ipyvue_flatsurf import Widget
            >>> W = Widget(S)
            >>> W.flow_components = [component]
            >>> W.flow_components
            [Cylinder with perimeter [3 → 1 → -3 → -1]]

        """
        return self._flow_components[0]

    def set_flow_components(self, flow_components, deformation=None):
        r"""
        Set the flow components currently visible in the widget.

        EXAMPLES::

            >>> from flatsurf import polygons, similarity_surfaces, GL2ROrbitClosure
            >>> from flatsurf.geometry.pyflatsurf_conversion import to_pyflatsurf
            >>> t = polygons.triangle(1, 1, 1)
            >>> B = similarity_surfaces.billiard(t)
            >>> S = B.minimal_cover('translation')
            >>> S = to_pyflatsurf(S)
            >>> deformation = S.eliminateMarkedPoints()
            >>> O = GL2ROrbitClosure(deformation.codomain())
            >>> D = next(O.decompositions(bound=64))

            >>> from ipyvue_flatsurf import Widget
            >>> W = Widget(S)
            >>> W.set_flow_components(D.components(), deformation.section())

        """
        flow_components = list(flow_components)
        self._flow_components = (flow_components, deformation)

        from ipyvue_flatsurf.encoding.flow_component_encoding import encode_flow_component
        self.flow_components_prop = []
        self.flow_components_prop = [VueFlatsurfWidget._to_yaml(encode_flow_component(component, deformation)) for component in flow_components]

    @flow_components.setter
    def flow_components(self, flow_components):
        self.set_flow_components(flow_components)

    @property
    def labels(self):
        r"""
        The kind of labels used for edges and half edges.

        EXAMPLES::

            >>> from flatsurf import translation_surfaces
            >>> S = translation_surfaces.square_torus();

            >>> from ipyvue_flatsurf import Widget
            >>> W = Widget(S)
            >>> W.labels
            'OUTER'

        Show numeric half edge labels::

            >>> W.labels = "NUMERIC"

        Only show alphhabetic labels on outer half edges::

            >>> W.labels = "OUTER"

        Show alphabetic labels on outer half edges and numeric labels on inner edges::

            >>> W.labels = "MIXED"

        Hide all labels::

            >>> W.labels = None

        """
        if self.show_numeric_labels_prop:
            if self.show_outer_labels_prop:
                return "MIXED"
            else:
                return "NUMERIC"
        else:
            if self.show_outer_labels_prop:
                return "OUTER"
            else:
                return None

    @labels.setter
    def labels(self, value):
        if value == "NUMERIC":
            self.show_numeric_labels_prop = True
            self.show_outer_labels_prop = False
        elif value == "OUTER":
            self.show_numeric_labels_prop = False
            self.show_outer_labels_prop = True
        elif value == "MIXED":
            self.show_numeric_labels_prop = True
            self.show_outer_labels_prop = True
        elif value is None:
            self.show_numeric_labels_prop = False
            self.show_outer_labels_prop = False
        else:
            raise ValueError(f"Unexpected labels kind '{value}'")

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
            '<comm :refs="$refs"><vue-flatsurf-widget ref="flatsurf" :triangulation="triangulation_prop" :snake-case="snake_case_prop" /></comm>'
        """
        def kebab(name): return name.replace('_', '-')
        return f"""<comm :refs="$refs"><vue-flatsurf-widget ref="flatsurf" { " ".join([f':{kebab(prop)}="{prop}_prop"' for prop in props]) } /></comm>"""

    @property
    async def svg(self):
        r"""
        Return the widget as a standalone SVG.

        EXAMPLES::

            >>> from flatsurf import translation_surfaces
            >>> S = translation_surfaces.square_torus();

            >>> from ipyvue_flatsurf import Widget
            >>> W = Widget(S)

        Unfortunately, this cannot be tested withuot an actual notebook
        running, see https://github.com/flatsurf/ipyvue-async/issues/2::

            >>> await W.svg  # doctest: +SKIP
            <svg ...>

        """
        import asyncio
        return await self.poll(self.query("flatsurf", "svg", return_when=asyncio.FIRST_COMPLETED))

    @property
    async def path(self):
        r"""
        The path drawn by the user or explicitly set.

        EXAMPLES::

            >>> from flatsurf import translation_surfaces
            >>> S = translation_surfaces.square_torus();

            >>> from ipyvue_flatsurf import Widget
            >>> W = Widget(S)

        Unfortunately, this cannot be tested withuot an actual notebook
        running, see https://github.com/flatsurf/ipyvue-async/issues/2::

            >>> await W.path  # doctest: +SKIP
            [...]

        Note that the path is not re-requested once it has been determined. To
        clear the path, you need to set it to `None`::

            >>> W.path = None
            >>> await W.path  # doctest: +SKIP

        The path can be given as a flatsurf path or as a list of flatsurf
        saddle connections::

            >>> import asyncio
            >>> W.path = []
            >>> asyncio.run(W.path)
            []

        """
        if self._path is None:
            self.action = "path"

            import asyncio

            path = await self.poll(self.query("flatsurf", "path", "completed", return_when=asyncio.FIRST_COMPLETED))

            # TODO: Unfortunately, we have to query explicitly for the layout,
            # see https://github.com/flatsurf/vue-flatsurf/issues/55. Also we
            # cannot be sure that we are getting the layout from the one that
            # gave us the path, see
            # https://github.com/flatsurf/ipyvue-async/issues/1.
            layout = await self.poll(self.query("flatsurf", "layout", "now", return_when=asyncio.FIRST_COMPLETED))

            S = self.triangulation

            inner = [edge.positive().id() for edge in S.edges() if layout['halfEdges'][str(edge)]['inner']]

            if len(path) < 2:
                raise NotImplementedError("Cannot represent trivial paths yet.")
            if 'vertex' not in path[0]:
                raise NotImplementedError("Cannot represent path that does not start at a vertex yet.")
            if 'vertex' not in path[-1]:
                raise NotImplementedError("Cannot represent path that does not end at a vertex yet.")

            from pyflatsurf import flatsurf

            path = [{
                'vertex': [flatsurf.HalfEdge(x) for x in p['vertex']]
            } if 'vertex' in p else {
                'halfEdge': flatsurf.HalfEdge(p['halfEdge'])
            } for p in path]

            connections = []

            # The input path consists of a list of points that are either at a
            # vertex or somewhere on a half edge.  Connections between vertex
            # points are in principle easy since we can exactly represent them
            # in libflatsurf as saddle connections.  However, a connection that
            # starts or ends inside a half edge has no correspondence in
            # libflatsurf (yet) so we need to rewrite it as a homotopic
            # sequence of connections of the first kind. Actually, we rewrite
            # it as a sequence of half edges, the simplest saddle connections.
            # To that end, we treat every half edge point as a point at the
            # vertex where this half edge starts.

            # The half edges that the path is crossing, i.e., the half edges
            # that we are allowed to cross when reconstructing an equivalent
            # representation of the path.
            inner = [flatsurf.HalfEdge(e) for e in inner] + [flatsurf.HalfEdge(-e) for e in inner]

            for source, target in zip(path, path[1:]):
                def source_faces(x):
                    if 'halfEdge' in x:
                        return [S.previousAtVertex(x['halfEdge'])]
                    else:
                        return x['vertex']

                def target_faces(x):
                    if 'halfEdge' in x:
                        return [x['halfEdge']]
                    else:
                        return x['vertex']

                # We now pretend that we start in one of the faces attached to
                # "start" and search for a path to a face attached to "target".
                paths = {}
                queue = []

                def enqueue_face(face, partial):
                    if face in paths:
                        return

                    paths[face] = partial
                    queue.append(face)

                    next = S.nextInFace(face)
                    enqueue_face(next, partial + [face])

                for source_face in source_faces(source):
                    enqueue_face(source_face, [])

                while queue:
                    face = queue.pop()
                    if face in inner:
                        enqueue_face(-face, paths[face] + [face])

                for target_face in target_faces(target):
                    if target_face in paths:
                        connections.extend(paths[target_face])
                        break
                else:
                    raise ValueError(f"Could not reconstruct the partial path from {source} to {target} that was reported by the frontend.")

            self._path = flatsurf.Path[type(S)]([flatsurf.SaddleConnection[type(S)](S, halfEdge) for halfEdge in connections])
        return self._path

    @path.setter
    def path(self, path):
        if self.action == "path":
            self.action = None
            self.action = "path"

        if path is None:
            self.paths_prop = []
            self._path = None
        else:
            from pyflatsurf import flatsurf
            Path = flatsurf.Path[type(self.triangulation)]
            path = Path(list(path))
            self._path = path

            from ipyvue_flatsurf.encoding.path_encoding import encode_path
            self.paths_prop = [VueFlatsurfWidget._to_yaml(encode_path(path))]

    @property
    def saddle_connections(self):
        r"""
        The saddle connections shown in the Widget.

        This is similar to path and only differs in that a path must be
        connection but a list of saddle connections might not be.

        EXAMPLES::

            >>> from flatsurf import translation_surfaces
            >>> S = translation_surfaces.square_torus();

            >>> from ipyvue_flatsurf import Widget
            >>> W = Widget(S)
            >>> W.saddle_connections
            []

            >>> W.saddle_connections = []

        """
        return self._saddle_connections

    @saddle_connections.setter
    def saddle_connections(self, connections):
        from ipyvue_flatsurf.encoding.saddle_connection_encoding import encode_saddle_connection
        self._saddle_connections = connections
        self.saddle_connections_prop = [VueFlatsurfWidget._to_yaml(encode_saddle_connection(connection)) for connection in connections]

    __force = Any(force_load, read_only=True).tag(sync=True, **widget_serialization)

    template = Unicode("").tag(sync=True)
    triangulation_prop = Unicode("").tag(sync=True)
    action_prop = Any(None).tag(sync=True)
    flow_components_prop = List([]).tag(sync=True)
    saddle_connections_prop = List([]).tag(sync=True)
    paths_prop = List([]).tag(sync=True)
    show_numeric_labels_prop = Bool(False).tag(sync=True)
    show_outer_labels_prop = Bool(True).tag(sync=True)

#*********************************************************************
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
#*********************************************************************
from ipywidgets.widgets.widget import widget_serialization
from traitlets import Unicode, Any, List
from ipyvue import VueTemplate

from .force_load import force_load

from flatsurf.geometry.translation_surface import TranslationSurface
from flatsurf.geometry.gl2r_orbit_closure import Decomposition

TranslationSurface._ipython_display_ = lambda self: FlatSurface(self)._ipython_display_()
Decomposition._ipython_display_ = lambda self: FlatSurface(self)._ipython_display_()

def surface_to_map(surface):
    return {
        "vertices": [list(he.id() for he in surface.atVertex(v)) for v in surface.vertices()],
        "vectors": {
            he.id(): {
                "x": float(surface.fromHalfEdge(he).x()),
                "y": float(surface.fromHalfEdge(he).y()),
            } for he in surface.halfEdges() if he.id() > 0
        }
    }

def _to_yaml(map):
    from io import StringIO
    buffer = StringIO()
    from ruamel.yaml import YAML
    yaml = YAML()
    yaml.dump(map, buffer)
    buffer.seek(0)
    return buffer.read().strip()

def component_to_map(component, deformation=None):
    surface = component.decomposition().surface()
    if deformation is not None:
        surface = deformation.codomain()

    touches = { halfEdge: [] for halfEdge in surface.halfEdges() }

    from dataclasses import dataclass

    def perimeter(component):
        return [connection for connection in component.perimeter() if component.cylinder() or (-connection).component() != component]

    def deform(connection):
        r"""
        Return the list of saddle connections that make up this saddle
        connection in the original surface before deforming it.
        """
        from pyflatsurf import flatsurf
        if deformation is None:
            return [connection]
        assert(connection.surface() == deformation.domain())
        connections = deformation(flatsurf.Path[type(connection.surface())](connection))
        connections = list(connections.value())

        vector = sum([c.vector() for c in connections], type(connections[0].vector())())
        assert(vector == connection.vector())
        return connections

    @dataclass
    class Touching:
        n: int
        step: object
        vector: object
        out: bool

        def __lt__(self, rhs):
            if isinstance(rhs, Crossing): return True
            if self.vector.ccw(rhs.vector) == 1: # = CW
                return True
            if self.vector.ccw(rhs.vector) == -1:
                return False
            if self.out and not rhs.out: return True
            if not self.out and rhs.out: return False
            assert False

    @dataclass
    class Crossing:
        # The sequential id of this crossing within the "step".
        n: int
        # The saddle connection which created this crossing.
        step: object
        # The location of the intersection.
        intersection: object
        # Whether this crossing is leaving or entering.
        # At the initial point of a saddle connection, there is a leaving
        # touching (out: True), then at every actual crossing, there is a pair
        # of crossings, one entering (out: False) and one leaving. Finally, at
        # the target of the saddle connection, there is an entering touching.
        out: bool

        def __lt__(self, rhs):
            if isinstance(rhs, Touching): return False
            if self.intersection < rhs.intersection:
                return True
            if rhs.intersection < self.intersection:
                return False
            if self.out and not rhs.out: return True
            if not self.out and rhs.out: return False
            assert False

    # After this loop, touches[halfEdge] lists the crossings that enter or
    # leave at this half edge.
    for connection in perimeter(component):
        for step in deform(connection.saddleConnection()):
            n = 1
            touches[step.source()].append(Touching(n, step, step.vector(), True))

            assert len(step.path()) == len((-step).path())
            for intersection, intersection_ in zip(step.path(), reversed((-step).path())):
                # TODO: Implement operator- for HalfEdgeIntersection so we do not need to -step
                assert intersection.halfEdge() == -intersection_.halfEdge()

                n+= 1
                touches[intersection.halfEdge()].append(Crossing(n, step, intersection, False))

                n+= 1
                touches[intersection_.halfEdge()].append(Crossing(n, step, intersection_, True))

            n+= 1
            touches[step.target()].append(Touching(n, step, -step.vector(), False))

    # Sort the touchings and crossings at the half edges such that they are in
    # the order as they appear along the half edge.
    for halfEdge in touches:
        touches[halfEdge].sort()

    # To be able to paint a picture of the entire component, we need to know
    # which half edges are inside the component and not immediately related to
    # the perimeter, e.g., because they are in a face that is completely in the
    # interior of the component.

    # For this, we determine of each half edge, whether it's beginning is part
    # of this component and whether its end is part of this component.
    start = {}
    end = {}

    for halfEdge in surface.halfEdges():
        if not touches[halfEdge]:
            previous = surface.previousAtVertex(halfEdge)
            if not touches[previous]:
                # This half edge is not directly involved in the perimeter. We can
                # only figure out in a second pass whether it is entirely inside or
                # outside the component.
                continue

            start[-halfEdge] = end[halfEdge] = start[halfEdge] = end[-halfEdge] = touches[previous][0].out
        else:
            crossings = [touch for touch in touches[halfEdge] if isinstance(touch, Crossing)]
            if crossings:
                # When we see a crossing going out of this half edge, we know that everything before it is in the component, and conversely.
                start[halfEdge] = crossings[0].out
                end[halfEdge] = not crossings[-1].out
                continue

            # The perimeter does not cross this half edge, it only touches the source vertex of this half edge.
            for touch in touches[halfEdge]:
                if touch.vector == surface.fromHalfEdge(halfEdge):
                    if touch.out:
                        # The half edge is part of the perimeter.
                        start[halfEdge] = end[halfEdge] = True
                        break
                    else:
                        # The half edge is not part of the perimeter, only it's opposite is.
                        start[halfEdge] = end[halfEdge] = False
                        break
            else:
                # The half edge is not part of the perimeter, the touching closest to the half edge decides whether it is inside or outside.
                start[halfEdge] = end[halfEdge] = not touches[halfEdge][-1].out

    # Walk around the vertices to fill in the blanks produced by half edges that do not show up in the perimeter at all.
    visited = set()
    def flood(source):
        if source in visited:
            return
        if source not in start:
            return

        visited.add(source)

        next = surface.nextAtVertex(source)

        if -next not in end:
            end[-next] = start[source]
            start[-next] = start[source]
            flood(-next)
            if next not in start:
                start[next] = start[source]
                end[next] = start[source]
                flood(next)

    for halfEdge in surface.halfEdges():
        flood(halfEdge)

    assert(all(halfEdge in start for halfEdge in surface.halfEdges()))
    assert(all(halfEdge in end for halfEdge in surface.halfEdges()))

    inside = [halfEdge for halfEdge in surface.halfEdges() if start[halfEdge] and end[halfEdge] and not any(isinstance(touch, Crossing) for touch in touches[halfEdge])]

    for halfEdge in touches:
        touches[halfEdge] = [(touch.step, touch.n, i) for (i, touch) in enumerate(touches[halfEdge])]

    touches = { step: sorted([ (touch[1], halfEdge.id(), touch[2]) for halfEdge in touches for touch in touches[halfEdge] if touch[0] == step ]) for connection in perimeter(component) for step in deform(connection.saddleConnection()) }

    return {
        "cylinder": bool(component.cylinder()),
        "perimeter": [{
            "source": step.source().id(),
            "target": step.target().id(),
            "vertical": connection.vertical(),
            "boundary": connection.component() != (-connection).component(), #TODO connection.boundary(),
            "vector": {
                "x": float(step.vector().x()),
                "y": float(step.vector().y()),
            },
            "crossings": [{
                "halfEdge": intersection.halfEdge().id(),
                "at": intersection.at(),
            } for intersection in step.path()],
            "touches": [ {
                "halfEdge": touch[1],
                "index": touch[2],
            } for touch in touches[step]],
        } for connection in perimeter(component) for step in deform(connection.saddleConnection())],
        "inside": [halfEdge.id() for halfEdge in inside],
    }

def decomposition_to_map(decomposition, deformation=None, components=None):
    map = surface_to_map(decomposition.surface() if deformation is None else deformation.codomain())
    if components is None:
        components = list(decomposition.components())
    # TODO: This does not make the coloring consistent. Can we get a canonical numbering somehow?
    components.sort(key = lambda c: c.area())
    map['components'] = [component_to_map(component, deformation) for component in list(components)]
    return map

class FlatSurface(VueTemplate):
    r"""
    A Flat Surfacae.

    >>> from flatsurf import translation_surfaces, polygons, similarity_surfaces
    >>> t = polygons.triangle(1, 1, 1)
    >>> B = similarity_surfaces.billiard(t)
    >>> S = B.minimal_cover('translation')
    >>> V = FlatSurface(S)

    """
    def __init__(self, surface, deformation=None, inner=[]):
        super().__init__()

        if isinstance(surface, Decomposition):
            surface = surface.decomposition
        if "flatsurf.FlowDecomposition" in str(type(surface)):
            map = decomposition_to_map(surface, deformation)
        elif "flatsurf.FlowComponent" in str(type(surface)):
            map = decomposition_to_map(surface.decomposition(), deformation, [surface])
        elif isinstance(surface, list):
            map = decomposition_to_map(surface[0].decomposition(), deformation, surface)
        else:
            if (deformation is not None):
                raise NotImplementedError()
            from flatsurf.geometry.pyflatsurf_conversion import to_pyflatsurf
            surface = to_pyflatsurf(surface)
            map = surface_to_map(surface)

        self.raw = _to_yaml(map)
        self.forced = inner

        self.svg = None

    __force = Any(force_load, read_only=True).tag(sync=True, **widget_serialization)

    template = Unicode(r"""
        <surface-viewer :raw="raw" :inner="forced" @update:inner="on_inner_update" @svg="on_svg" />
    """).tag(sync=True)

    def vue_on_inner_update(self, inner):
        self.inner = inner

    def vue_on_svg(self, svg):
        self.svg = svg

    inner = List([]).tag(sync=True)

    raw = Unicode("").tag(sync=True)

    forced = List([]).tag(sync=True)

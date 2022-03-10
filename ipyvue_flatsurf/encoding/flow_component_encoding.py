r"""
Encodes a flatsurf FlowComponent in a format that is understood by vue-flatsurf.
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

from dataclasses import dataclass
from functools import cache


def encode_flow_component(component, deformation=None):
    r"""
    Return the flow component encoded as a primitive type.

    EXAMPLES::

        >>> from flatsurf import translation_surfaces, GL2ROrbitClosure
        >>> S = translation_surfaces.square_torus()
        >>> O = GL2ROrbitClosure(S)
        >>> D = next(O.decompositions(bound=64))
        >>> component = D.components()[0]
        >>> encode_flow_component(component)
        {'cylinder': True, 'perimeter': [...], 'inside': [1, -1, 2, -2, 3, -3]}

    Using a deformation, a flow component can also be pulled back from a
    deformed surface::

        >>> from flatsurf import polygons, similarity_surfaces, GL2ROrbitClosure
        >>> from flatsurf.geometry.pyflatsurf_conversion import to_pyflatsurf
        >>> t = polygons.triangle(1, 1, 1)
        >>> B = similarity_surfaces.billiard(t)
        >>> S = B.minimal_cover('translation')
        >>> deformation = to_pyflatsurf(S).eliminateMarkedPoints()
        >>> O = GL2ROrbitClosure(deformation.codomain())
        >>> D = next(O.decompositions(bound=64))
        >>> component = D.components()[0]
        >>> encode_flow_component(component, deformation=deformation.section())
        {'cylinder': True, 'perimeter': [...], 'inside': [1, -1, 3, -3, 4, -4, 6, -6, 7, -7, 8, -8, 9, -9]}

    """
    return Encoder(component, deformation).encoded


class Encoder:
    r"""
    Helper structure to encode a flow component as a promitive type.
    """

    def __init__(self, component, deformation=None):
        self.component = component
        self.deformation = deformation

        if self.deformation is None:
            self.surface = self.component.decomposition().surface()
        else:
            self.surface = self.deformation.codomain()

    @property
    def encoded(self):
        r"""
        Return an encoded version of this flow component.
        """
        start, end = self.in_component

        inside = [halfEdge for halfEdge in self.surface.halfEdges() if start[halfEdge] and end[halfEdge] and not any(isinstance(touch, Crossing) for touch in self.touches[halfEdge])]

        touches = {halfEdge: [(touch.step, touch.n, i) for (i, touch) in enumerate(self.touches[halfEdge])] for halfEdge in self.touches}

        touches = {step: sorted([(touch[1], halfEdge.id(), touch[2]) for halfEdge in touches for touch in touches[halfEdge] if touch[0] == step]) for connection in self.perimeter for step in self.pullback(connection.saddleConnection())}

        from ipyvue_flatsurf.encoding.saddle_connection_encoding import encode_saddle_connection

        return {
            "cylinder": bool(self.component.cylinder()),
            "perimeter": [dict(
                vertical=connection.vertical(),
                boundary=connection.boundary(),
                touches=[{
                    "halfEdge": touch[1],
                    "index": touch[2],
                } for touch in touches[step]],
                **encode_saddle_connection(step),
            ) for connection in self.perimeter for step in self.pullback(connection.saddleConnection())],
            "inside": [halfEdge.id() for halfEdge in inside],
        }

    @property
    @cache
    def touches(self):
        r"""
        Return for each half edge the touches and crossings of a flow
        connection with this half edge.

        EXAMPLES::

            >>> from flatsurf import translation_surfaces, GL2ROrbitClosure
            >>> S = translation_surfaces.square_torus()
            >>> O = GL2ROrbitClosure(S)
            >>> D = next(O.decompositions(bound=64))
            >>> component = D.components()[0]

            >>> from pyflatsurf import flatsurf
            >>> Encoder(component).touches[flatsurf.HalfEdge(1)]
            [Touching(n=1, step=1, out=True, vector=(1, 1)), Touching(n=2, step=-1, out=False, vector=(1, 1))]

        ::

            >>> S = translation_surfaces.mcmullen_L(1, 1, 1, 1)
            >>> O = GL2ROrbitClosure(S)
            >>> D = O.decomposition((1, 0))
            >>> component = D.components()[0]

            >>> from ipyvue_flatsurf.encoding.flow_component_encoding import Encoder
            >>> encoder = Encoder(component)
            >>> encoder.touches[flatsurf.HalfEdge(1)]
            [Touching(n=1, step=1, out=True, vector=(1, 1)), Touching(n=2, step=-1, out=False, vector=(1, 1))]


        """
        touches = {halfEdge: [] for halfEdge in self.surface.halfEdges()}

        # After this loop, touches[halfEdge] lists the crossings that enter or
        # leave at this half edge.
        for connection in self.perimeter:
            for step in self.pullback(connection.saddleConnection()):
                n = 1
                touches[step.source()].append(Touching(n=n, step=step, vector=step.vector(), out=True))

                assert len(step.path()) == len((-step).path())
                for intersection, intersection_ in zip(step.path(), reversed((-step).path())):
                    # It seems that this could be simplified if we had a HalfEdgeIntersection::operator-.
                    assert intersection.halfEdge() == -intersection_.halfEdge()

                    n += 1
                    touches[intersection.halfEdge()].append(Crossing(n=n, step=step, intersection=intersection, out=False))

                    n += 1
                    touches[intersection_.halfEdge()].append(Crossing(n=n, step=step, intersection=intersection_, out=True))

                n += 1
                touches[step.target()].append(Touching(n=n, step=step, vector=-step.vector(), out=False))

        # Sort the touchings and crossings at the half edges such that they are in
        # the order as they appear along the half edge.
        for halfEdge in touches:
            touches[halfEdge].sort()

        return touches

    def pullback(self, connection):
        r"""
        Return the list of saddle connections that make up this saddle
        connection in the original surface before deforming it.

        EXAMPLES::

            >>> from flatsurf import translation_surfaces, GL2ROrbitClosure
            >>> S = translation_surfaces.square_torus()
            >>> O = GL2ROrbitClosure(S)
            >>> D = next(O.decompositions(bound=64))
            >>> component = D.components()[0]

            >>> from ipyvue_flatsurf.encoding.flow_component_encoding import Encoder
            >>> encoder = Encoder(component)
            >>> encoder.perimeter
            [3, 1, -3, -1]
            >>> [encoder.pullback(connection) for connection in encoder.perimeter]
            [[3], [1], [-3], [-1]]

        ::

            >>> from flatsurf import polygons, similarity_surfaces
            >>> from flatsurf.geometry.pyflatsurf_conversion import to_pyflatsurf
            >>> t = polygons.triangle(1, 1, 1)
            >>> B = similarity_surfaces.billiard(t)
            >>> S = B.minimal_cover('translation')
            >>> deformation = to_pyflatsurf(S).eliminateMarkedPoints()
            >>> O = GL2ROrbitClosure(deformation.codomain())
            >>> D = next(O.decompositions(bound=64))
            >>> component = D.components()[0]

            >>> encoder = Encoder(component, deformation=deformation.section())
            >>> encoder.perimeter
            [3, 1, -3, -1]
            >>> [encoder.pullback(connection.saddleConnection()) for connection in encoder.perimeter]
            [[((3/2 ~ 1.5000000), (1/2*c ~ 0.86602540)) from 1 to 6], [((-3/2 ~ -1.5000000), (1/2*c ~ 0.86602540)) from -9 to 4], [((-3/2 ~ -1.5000000), (-1/2*c ~ -0.86602540)) from 6 to 1], [((3/2 ~ 1.5000000), (-1/2*c ~ -0.86602540)) from 4 to -9]]

        """
        from pyflatsurf import flatsurf
        if self.deformation is None:
            return [connection]
        assert(connection.surface() == self.deformation.domain())
        connections = self.deformation(flatsurf.Path[type(connection.surface())](connection))
        connections = list(connections.value())

        vector = sum([c.vector() for c in connections], type(connections[0].vector())())
        assert(vector == connection.vector())
        return connections

    @property
    @cache
    def perimeter(self):
        r"""
        The relevant perimeter of this component.

        This is a sequence of saddle connections that make up the perimeter of
        this component. Non-cylinders often contain lots of saddle connections
        that were created by the Rauzy induction but are just internal to the
        component, i.e., the component is on both sides of the connection.

        We exclude such connections since they are usually of no interest.

        TODO: This is maybe not the right thing to do for non-cylinders. In
        particular, this breaks when there is only one minimal or
        undetermined component as this excludes everything. See
        https://github.com/flatsurf/ipyvue-flatsurf/issues/46.

        EXAMPLES::

            >>> from flatsurf import translation_surfaces, GL2ROrbitClosure
            >>> S = translation_surfaces.square_torus()
            >>> O = GL2ROrbitClosure(S)
            >>> D = next(O.decompositions(bound=64))
            >>> component = D.components()[0]

            >>> from ipyvue_flatsurf.encoding.flow_component_encoding import Encoder
            >>> encoder = Encoder(component)
            >>> encoder.perimeter
            [3, 1, -3, -1]

        ::

            >>> S = translation_surfaces.mcmullen_L(1, 1, 1, 1)
            >>> O = GL2ROrbitClosure(S)
            >>> D = O.decomposition((1, 0))
            >>> component = D.components()[0]

            >>> from ipyvue_flatsurf.encoding.flow_component_encoding import Encoder
            >>> encoder = Encoder(component)
            >>> encoder.perimeter
            [-1, -5, -8, 1, 2, 8]


        """
        return [connection for connection in self.component.perimeter() if
                self.component.cylinder() or connection.boundary()]

    @property
    @cache
    def in_component(self):
        r"""
        Return for each half edge whether its beginning is part this component
        and whether its end is part of this component.

        To be able to paint a picture of the entire component, we need to know
        which half edges are inside the component and not immediately related to
        the perimeter, e.g., because they are in a face that is completely in the
        interior of the component.

        EXAMPLES::

            >>> from flatsurf import translation_surfaces, GL2ROrbitClosure
            >>> S = translation_surfaces.square_torus()
            >>> O = GL2ROrbitClosure(S)
            >>> D = next(O.decompositions(bound=64))
            >>> component = D.components()[0]

            >>> from ipyvue_flatsurf.encoding.flow_component_encoding import Encoder
            >>> encoder = Encoder(component)
            >>> encoder.in_component
            ({1: True, -1: True, -2: True, 2: True, 3: True, -3: True}, {1: True, -1: True, 2: True, -2: True, 3: True, -3: True})

        ::

            >>> S = translation_surfaces.mcmullen_L(1, 1, 1, 1)
            >>> O = GL2ROrbitClosure(S)
            >>> D = O.decomposition((1, 0))
            >>> component = D.components()[0]

            >>> from ipyvue_flatsurf.encoding.flow_component_encoding import Encoder
            >>> encoder = Encoder(component)
            >>> encoder.in_component[0]
            {1: True, -1: True, 2: True, -2: False, 3: True, -3: True, -4: False, 4: False, 5: False, -5: True, -7: True, 7: True, 8: True, -8: True, -9: True, 9: True, 6: False, -6: False}
            >>> encoder.in_component[1]
            {1: True, -1: True, 2: True, -2: False, -3: True, 3: True, 4: False, -4: False, 5: False, -5: True, 7: True, -7: True, 8: True, -8: True, 9: True, -9: True, 6: False, -6: False}


        """
        start = {}
        end = {}

        for halfEdge in self.surface.halfEdges():
            if not self.touches[halfEdge]:
                previous = self.surface.previousAtVertex(halfEdge)
                if not self.touches[previous]:
                    # This half edge is not directly involved in the perimeter. We can
                    # only figure out in a second pass whether it is entirely inside or
                    # outside the component.
                    continue

                start[-halfEdge] = end[halfEdge] = start[halfEdge] = end[-halfEdge] = self.touches[previous][0].out
            else:
                crossings = [touch for touch in self.touches[halfEdge] if isinstance(touch, Crossing)]
                if crossings:
                    # When we see a crossing going out of this half edge, we know that everything before it is in the component, and conversely.
                    start[halfEdge] = crossings[0].out
                    end[halfEdge] = not crossings[-1].out
                    continue

                # The perimeter does not cross this half edge, it only touches the source vertex of this half edge.
                for touch in self.touches[halfEdge]:
                    if touch.vector == self.surface.fromHalfEdge(halfEdge):
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
                    start[halfEdge] = end[halfEdge] = not self.touches[halfEdge][-1].out

        # Walk around the vertices to fill in the blanks produced by half edges that do not show up in the perimeter at all.
        visited = set()

        def flood(source):
            if source in visited:
                return
            if source not in start:
                return

            visited.add(source)

            next = self.surface.nextAtVertex(source)

            if -next not in end:
                end[-next] = start[source]
                start[-next] = start[source]
                flood(-next)
                if next not in start:
                    start[next] = start[source]
                    end[next] = start[source]
                    flood(next)

        for halfEdge in self.surface.halfEdges():
            flood(halfEdge)

        assert all(halfEdge in start for halfEdge in self.surface.halfEdges()), start
        assert all(halfEdge in end for halfEdge in self.surface.halfEdges()), end

        return start, end


@dataclass
class TouchingOrCrossing:
    r"""
    Base class for touchings and crossings, i.e., representing the moment when
    a flow connection hits the triangulation.
    """
    # The sequential id of this touching or crossing within the "step".
    n: int
    # The saddle connection which created this touching or crossing.
    step: object
    # Whether this crossing is leaving or entering.
    # At the initial point of a saddle connection, there is a leaving
    # touching (out: True), then at every actual crossing, there is a pair
    # of crossings, one entering (out: False) and one leaving. Finally, at
    # the target of the saddle connection, there is an entering touching.
    out: bool


@dataclass
class Touching(TouchingOrCrossing):
    r"""
    A touching of a flow connection and the triangulation, i.e., the moment
    when flaw connection starts/ends at a vertex.
    """
    # The direction of the saddle connection that created this tuoching.
    vector: object

    def __lt__(self, rhs):
        if isinstance(rhs, Crossing):
            return True
        if self.vector.ccw(rhs.vector) == 1:  # = CW
            return True
        if self.vector.ccw(rhs.vector) == -1:
            return False
        if self.out and not rhs.out:
            return True
        if not self.out and rhs.out:
            return False
        assert False


@dataclass
class Crossing(TouchingOrCrossing):
    r"""
    A crossing of a flow connection and the triangulation, i.e., the moment
    when flaw connection crosses over a half edge.
    """
    # The location of the intersection.
    intersection: object

    def __lt__(self, rhs):
        if isinstance(rhs, Touching):
            return False
        if self.intersection < rhs.intersection:
            return True
        if rhs.intersection < self.intersection:
            return False
        if self.out and not rhs.out:
            return True
        if not self.out and rhs.out:
            return False
        assert False

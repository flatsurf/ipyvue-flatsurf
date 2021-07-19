from ipywidgets.widgets.widget import widget_serialization
from traitlets import Unicode, Any
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

    def deform(connection):
        from pyflatsurf import flatsurf
        if deformation is None:
            return [connection]
        assert(connection.surface() == deformation.domain())
        connections = deformation(flatsurf.Path[type(connection.surface())](connection))
        return list(connections.value())

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
        n: int
        step: object
        intersection: object
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

    for connection in component.perimeter():
        for step in deform(connection.saddleConnection()):
            n = 1
            touches[step.source()].append(Touching(n, step, step.vector(), True))

            for intersection, intersection_ in zip(step.path(), reversed((-step).path())):
                # TODO: Implement operator- for HalfEdgeIntersection so we do not need to -step
                assert intersection.halfEdge() == -intersection_.halfEdge()

                n+= 1
                touches[intersection.halfEdge()].append(Crossing(n, step, intersection, False))

                n+= 1
                touches[intersection_.halfEdge()].append(Crossing(n, step, intersection_, True))

            n+= 1
            touches[step.target()].append(Touching(n, step, -step.vector(), False))

    for halfEdge in touches:
        touches[halfEdge].sort()
        touches[halfEdge] = [(touch.step, touch.n, i) for (i, touch) in enumerate(touches[halfEdge])]

    touches = { step: sorted([ (touch[1], halfEdge.id(), touch[2]) for halfEdge in touches for touch in touches[halfEdge] if touch[0] == step ]) for connection in component.perimeter() for step in deform(connection.saddleConnection()) }

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
        } for connection in component.perimeter() for step in deform(connection.saddleConnection())]
    }

def decomposition_to_map(decomposition, deformation=None):
    map = surface_to_map(decomposition.surface() if deformation is None else deformation.codomain())
    map['components'] = [component_to_map(component, deformation) for component in list(decomposition.components())]
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
    def __init__(self, surface, deformation=None):
        super().__init__()

        if isinstance(surface, Decomposition):
            surface = surface.decomposition
        if "flatsurf.FlowDecomposition" in str(type(surface)):
            map = decomposition_to_map(surface, deformation)
        else:
            from flatsurf.geometry.pyflatsurf_conversion import to_pyflatsurf
            surface = to_pyflatsurf(surface)
            map = surface_to_map(surface)
            
        self.raw = _to_yaml(map)

    __force = Any(force_load, read_only=True).tag(sync=True, **widget_serialization)

    template = Unicode(r"""
    <surface-viewer :raw="raw" />
    """).tag(sync=True)

    raw = Unicode("").tag(sync=True)

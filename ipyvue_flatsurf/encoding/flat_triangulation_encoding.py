r"""
Encodes a flatsurf FlatTriangulation in a format that is understood by vue-flatsurf.
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


def encode_flat_triangulation(triangulation):
    r"""
    Return the flat triangulation encoded as a primitive type.

    EXAMPLES::

        >>> from flatsurf import translation_surfaces
        >>> S = translation_surfaces.square_torus()

        >>> from flatsurf.geometry.pyflatsurf_conversion import to_pyflatsurf
        >>> T = to_pyflatsurf(S)

        >>> encode_flat_triangulation(T) == {'vertices': [[1, -3, 2, -1, 3, -2]], 'vectors': {1: {'x': 1.0, 'y': 1.0}, 2: {'x': -1.0, 'y': 0.0}, 3: {'x': 0.0, 'y': -1.0}}}
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

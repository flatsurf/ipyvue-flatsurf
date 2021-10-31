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

        >>> from flatsurf import translation_surfaces, polygons, similarity_surfaces
        >>> t = polygons.triangle(1, 1, 1)
        >>> B = similarity_surfaces.billiard(t)
        >>> S = B.minimal_cover('translation')

        >>> from flatsurf.geometry.pyflatsurf_conversion import to_pyflatsurf
        >>> T = to_pyflatsurf(S)

        >>> encode_flat_triangulation(T) == {
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

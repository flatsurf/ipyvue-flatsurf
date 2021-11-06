r"""
Encodes a flatsurf SaddleConnection in a format that is understood by vue-flatsurf.
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


def encode_saddle_connection(connection):
    r"""
    Return the saddle connection as a primitive type.

    EXAMPLES::

        >>> from flatsurf import translation_surfaces
        >>> S = translation_surfaces.square_torus()

        >>> from flatsurf.geometry.pyflatsurf_conversion import to_pyflatsurf
        >>> T = to_pyflatsurf(S)
        >>> connection = next(iter(T.connections()))
        >>> encode_saddle_connection(connection)
        {'source': 1, 'target': -1, 'vector': {'x': 1.0, 'y': 1.0}, 'crossings': []}

    """
    return {
        "source": connection.source().id(),
        "target": connection.target().id(),
        "vector": {
            "x": float(connection.vector().x()),
            "y": float(connection.vector().y()),
        },
        "crossings": [{
           "halfEdge": intersection.halfEdge().id(),
           "at": intersection.at(),
        } for intersection in connection.path()]
    }

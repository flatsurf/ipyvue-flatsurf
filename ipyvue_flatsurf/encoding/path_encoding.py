r"""
Encodes a flatsurf Path in a format that is understood by vue-flatsurf.
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

from ipyvue_flatsurf.encoding.saddle_connection_encoding import encode_saddle_connection


def encode_path(path):
    r"""
    Return the path encoded as a primitive type.

    EXAMPLES::

        >>> from flatsurf import translation_surfaces, GL2ROrbitClosure
        >>> S = translation_surfaces.square_torus()
        >>> O = GL2ROrbitClosure(S)
        >>> D = next(O.decompositions(bound=64))
        >>> component = D.components()[0]
        >>> perimeter = component.perimeter()

        >>> from pyflatsurf import flatsurf
        >>> from flatsurf.geometry.pyflatsurf_conversion import to_pyflatsurf
        >>> path = flatsurf.Path[type(to_pyflatsurf(S))]([connection.saddleConnection() for connection in perimeter])
        >>> encode_path(path)
        {'connections': ...}

    """
    return {
        'connections': [encode_saddle_connection(connection) for connection in path]
    }

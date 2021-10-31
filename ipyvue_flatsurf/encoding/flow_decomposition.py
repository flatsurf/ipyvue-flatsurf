r"""
Encodes a flatsurf FlowDecomposition in a format that is understood by vue-flatsurf.
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

from ipyvue_flatsurf.encoding.flow_component import encode_flow_component


def encode_flow_decomposition(decomposition, deformation=None):
    r"""
    Return the flow decomposition encoded as a primitive type.

    EXAMPLES::

        >>> from flatsurf import translation_surfaces, polygons, similarity_surfaces, GL2ROrbitClosure
        >>> t = polygons.triangle(1, 1, 1)
        >>> B = similarity_surfaces.billiard(t)
        >>> S = B.minimal_cover('translation')
        >>> O = GL2ROrbitClosure(S)
        >>> D = next(O.decompositions(bound=64))
        >>> encode_flow_decomposition(D.decomposition)
        [{'cylinder': True, 'perimeter': [...], 'inside': [1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6, 7, -7, 8, -8, 9, -9]}]

    """
    return [encode_flow_component(component, deformation) for component in decomposition.components()]

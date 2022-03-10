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

from ipyvue_flatsurf.encoding.flow_component_encoding import encode_flow_component


def encode_flow_decomposition(decomposition, deformation=None):
    r"""
    Return the flow decomposition encoded as a primitive type.

    EXAMPLES::

        >>> from flatsurf import translation_surfaces, GL2ROrbitClosure
        >>> S = translation_surfaces.square_torus()
        >>> O = GL2ROrbitClosure(S)
        >>> D = next(O.decompositions(bound=64))
        >>> encode_flow_decomposition(D)
        [{'cylinder': True, 'perimeter': [...], 'inside': [1, -1, 2, -2, 3, -3]}]

    """
    return [encode_flow_component(component, deformation) for component in decomposition.components()]

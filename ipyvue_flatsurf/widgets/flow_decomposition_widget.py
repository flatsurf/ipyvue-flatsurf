r"""
A Jupyter Widget for a sage-flatsurf Flow Decomposition.

EXAMPLES:

    >>> from flatsurf import translation_surfaces, GL2ROrbitClosure
    >>> S = translation_surfaces.square_torus()
    >>> O = GL2ROrbitClosure(S)
    >>> D = next(O.decompositions(bound=64))
    >>> FlowDecompositionWidget(D)
    FlowDecompositionWidget(...)

Typically, this module is not used directly, but the widget created through the
`Widget` helper::

    >>> from ipyvue_flatsurf import Widget
    >>> Widget(D)
    FlowDecompositionWidget(...)

We can also pull back components through a deformation such as the one that is
eliminating marked points::

    >>> from flatsurf import polygons, similarity_surfaces, GL2ROrbitClosure
    >>> from flatsurf.geometry.pyflatsurf_conversion import to_pyflatsurf
    >>> t = polygons.triangle(1, 1, 1)
    >>> B = similarity_surfaces.billiard(t)
    >>> S = B.minimal_cover('translation')
    >>> deformation = to_pyflatsurf(S).eliminateMarkedPoints()
    >>> O = GL2ROrbitClosure(deformation.codomain())
    >>> D = next(O.decompositions(bound=64))
    >>> FlowDecompositionWidget(D, deformation=deformation.section())
    FlowDecompositionWidget(...)

::

    >>> Widget(D, deformation=deformation.section())
    FlowDecompositionWidget(...)

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

from ipyvue_flatsurf.widgets.vue_flatsurf_widget import VueFlatsurfWidget


class FlowDecompositionWidget(VueFlatsurfWidget):
    def __init__(self, decomposition, deformation=None):
        if deformation is not None:
            triangulation = deformation.codomain()
        else:
            triangulation = decomposition.surface()
        VueFlatsurfWidget.__init__(self, triangulation)

        self.set_flow_components(decomposition.components(), deformation)

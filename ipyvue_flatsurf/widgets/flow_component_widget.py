r"""
A Jupyter Widget for one or several sage-flatsurf Flow Components.

EXAMPLES:

    >>> from flatsurf import translation_surfaces, GL2ROrbitClosure
    >>> S = translation_surfaces.square_torus()
    >>> O = GL2ROrbitClosure(S)
    >>> D = next(O.decompositions(bound=64))
    >>> components = D.components()
    >>> FlowComponentWidget(list(components))
    FlowComponentWidget...)

Typically, this module is not used directly, but the widget created through the
`Widget` helper::

    >>> from ipyvue_flatsurf import Widget
    >>> Widget(components)
    FlowComponentWidget(...)

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
    >>> components = D.components()
    >>> FlowComponentWidget(components, deformation=deformation.section())
    FlowComponentWidget(...)

::

    >>> Widget(components, deformation=deformation.section())
    FlowComponentWidget(...)

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


class FlowComponentWidget(VueFlatsurfWidget):
    def __init__(self, components, deformation=None):
        from ipyvue_flatsurf.widget import is_iterable
        if not is_iterable(components):
            components = [components]

        components = list(components)

        if len(components) == 0:
            raise ValueError("cannot render a widget for zero flow components")

        if deformation is not None:
            triangulation = deformation.codomain()
        else:
            triangulation = components[0].decomposition().surface()
        VueFlatsurfWidget.__init__(self, triangulation)

        self.set_flow_components(components, deformation)

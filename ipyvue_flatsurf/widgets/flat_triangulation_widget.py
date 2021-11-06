r"""
A Jupyter Widget for a flatsurf Flat Triangulation.

EXAMPLES::

    >>> from flatsurf import translation_surfaces
    >>> S = translation_surfaces.square_torus()
    >>> from flatsurf.geometry.pyflatsurf_conversion import to_pyflatsurf
    >>> S = to_pyflatsurf(S)
    >>> FlatTriangulationWidget(S)
    FlatTriangulationWidget(...)

Typically, this module is not used directly, but the widget created through the
`Widget` helper::

    >>> from ipyvue_flatsurf import Widget
    >>> Widget(S)
    FlatTriangulationWidget(...)

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


class FlatTriangulationWidget(VueFlatsurfWidget):
    def __init__(self, triangulation):
        VueFlatsurfWidget.__init__(self, triangulation)

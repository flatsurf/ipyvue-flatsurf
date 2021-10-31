r"""
Provide widgets for flatsurf.

This module provides a generic `Widget` command to create a Jupyter Widget for
the various objects in flatsurf, pyflatsurf, and sage-flatsurf. It also sets
display hooks so these widgets are shown automatically in Jupyter Notebooks.

EXAMPLES::

    >>> from flatsurf import translation_surfaces, polygons, similarity_surfaces
    >>> t = polygons.triangle(1, 1, 1)
    >>> B = similarity_surfaces.billiard(t)
    >>> S = B.minimal_cover('translation')

This module provides an explicit `Widget` command to create a widget::

    >>> from ipyvue_flatsurf.widget import Widget
    >>> Widget(S)
    TranslationSurfaceWidget(...)

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

from flatsurf.geometry.translation_surface import TranslationSurface
from flatsurf.geometry.gl2r_orbit_closure import Decomposition


def Widget(x):
    r"""
    Create a widget from `x`.

    EXAMPLES:

    A widget from a sage-flatsurf translation surface::

    >>> from flatsurf import translation_surfaces, polygons, similarity_surfaces
    >>> t = polygons.triangle(1, 1, 1)
    >>> B = similarity_surfaces.billiard(t)
    >>> S = B.minimal_cover('translation')
    >>> Widget(S)
    TranslationSurfaceWidget(...)

    """
    if isinstance(x, TranslationSurface):
        from ipyvue_flatsurf.widgets.translation_surface_widget import TranslationSurfaceWidget
        return TranslationSurfaceWidget(x)

    raise TypeError(f"No flatsurf widget available for {type(x)}")


TranslationSurface._ipython_display_ = lambda self: Widget(self)._ipython_display_()

r"""
Provide widgets for flatsurf.

This module provides a generic `Widget` command to create a Jupyter Widget for
the various objects in flatsurf, pyflatsurf, and sage-flatsurf. It also sets
display hooks so these widgets are shown automatically in Jupyter Notebooks.

EXAMPLES::

    >>> from flatsurf import translation_surfaces
    >>> S = translation_surfaces.square_torus()

This module provides an explicit `Widget` command to create a widget::

    >>> from ipyvue_flatsurf.widget import Widget
    >>> Widget(S)
    TranslationSurfaceWidget(...)

"""
# ********************************************************************
#  This file is part of ipyvue-flatsurf.
#
#        Copyright (C) 2021-2022 Julian Rüth
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


def Widget(x, *args, **kwargs):
    r"""
    Create a widget from `x`.

    EXAMPLES:

    A widget from a sage-flatsurf translation surface::

    >>> from flatsurf import translation_surfaces
    >>> S = translation_surfaces.square_torus()
    >>> Widget(S)
    TranslationSurfaceWidget(...)

    A widget for a sage-flatsurf flow decomposition::

    >>> from flatsurf import GL2ROrbitClosure
    >>> O = GL2ROrbitClosure(S)
    >>> D = next(O.decompositions(bound=64))
    >>> Widget(D)
    FlowDecompositionWidget(...)

    A widget for a flatsurf flow component::

    >>> component = D.components()[0]
    >>> Widget(component)
    FlowComponentWidget(...)

    A widget for a collection of flow components::

    >>> components = D.components()
    >>> Widget(components)
    FlowComponentWidget(...)

    """
    if isinstance(x, TranslationSurface):
        from ipyvue_flatsurf.widgets.translation_surface_widget import TranslationSurfaceWidget
        return TranslationSurfaceWidget(x, *args, **kwargs)

    if is_flow_decomposition(x):
        from ipyvue_flatsurf.widgets.flow_decomposition_widget import FlowDecompositionWidget
        return FlowDecompositionWidget(x, *args, **kwargs)

    if is_flow_component(x):
        from ipyvue_flatsurf.widgets.flow_component_widget import FlowComponentWidget
        return FlowComponentWidget(x, *args, **kwargs)

    if is_flat_triangulation(x):
        from ipyvue_flatsurf.widgets.flat_triangulation_widget import FlatTriangulationWidget
        return FlatTriangulationWidget(x, *args, **kwargs)

    if is_iterable(x) and all([is_flow_component(y) for y in x]):
        from ipyvue_flatsurf.widgets.flow_component_widget import FlowComponentWidget
        return FlowComponentWidget(list(x), *args, **kwargs)

    raise TypeError(f"No flatsurf widget available for {type(x)}")


def is_iterable(x):
    r"""
    Return whether `x` is iterable.
    """
    from collections.abc import Iterable
    if isinstance(x, Iterable):
        return True
    try:
        next(iter(x))
    except TypeError:
        return False
    return True


def is_flow_component(x):
    r"""
    Return whether `x` is a flow component.

    TODO: This method should go into pyflatsurf, see https://github.com/flatsurf/flatsurf/issues/279.

    EXAMPLES::

        >>> from flatsurf import translation_surfaces
        >>> S = translation_surfaces.square_torus()
        >>> is_flow_component(S)
        False

        >>> from flatsurf.geometry.pyflatsurf_conversion import to_pyflatsurf
        >>> S = to_pyflatsurf(S)
        >>> is_flow_component(S)
        False

    """
    return "flatsurf.FlowComponent<" in str(type(x))


def is_flow_decomposition(x):
    r"""
    Return whether `x` is a flow decomposition.

    TODO: This method should go into pyflatsurf, see https://github.com/flatsurf/flatsurf/issues/279.

    EXAMPLES::

        >>> from flatsurf import translation_surfaces
        >>> S = translation_surfaces.square_torus()
        >>> is_flow_decomposition(S)
        False

        >>> from flatsurf.geometry.pyflatsurf_conversion import to_pyflatsurf
        >>> S = to_pyflatsurf(S)
        >>> is_flow_decomposition(S)
        False

    """
    return "flatsurf.FlowDecomposition<" in str(type(x))


def is_flat_triangulation(x):
    r"""
    Return whether `x` is a flat triangulation.

    TODO: This method should go into pyflatsurf, see https://github.com/flatsurf/flatsurf/issues/279.

    EXAMPLES::

        >>> from flatsurf import translation_surfaces
        >>> S = translation_surfaces.square_torus()
        >>> is_flat_triangulation(S)
        False

        >>> from flatsurf.geometry.pyflatsurf_conversion import to_pyflatsurf
        >>> is_flat_triangulation(to_pyflatsurf(S))
        True

    """
    return "flatsurf.FlatTriangulation<" in str(type(x))


TranslationSurface._ipython_display_ = lambda self: Widget(self)._ipython_display_()

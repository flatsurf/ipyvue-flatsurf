r"""
Jupyter Widgets for flatsurf.

This package adds display hooks for some of the objects in flatsurf, pyflatsurf,
and sage-flatsurf.

EXAMPLES:

Importing this module adds display hooks::

    >>> import ipyvue_flatsurf

They get called automatically if a cell ends with such an object::

    >>> from flatsurf import translation_surfaces
    >>> S = translation_surfaces.square_torus()
    >>> S
    Translation Surface in H_1(0) built from a square

Running the above in a Jupyter notebook calls the `_repr_mimebundle_` hook and
displays an actual widget instead::

    >>> S._repr_mimebundle_()
    Output()
    {...}

"""
# ********************************************************************
#  This file is part of ipyvue-flatsurf.
#
#        Copyright (C) 2021-2025 Julian Rüth
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

from ipyvue_flatsurf.widget import Widget

_ = Widget  # silence pyflakes

version_info = (0, 6, 3)
__version__ = "0.6.3"

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
    TranslationSurface built from 1 polygon

Running the above in a Jupyter notebook calls the `_ipython_display_` hook and
displays an actual widget instead::

    >>> S._ipython_display_()
    {...}

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

from ipyvue_flatsurf.widget import Widget

Widget  # silence pyflakes


version_info = (0, 5, 5)
__version__ = "0.5.5"


def _jupyter_labextension_paths():
    r"""
    Called by JupyterLab to find out which JavaScript assets need to be copied.
    """
    # The command `jupyter labextension build` creates a package in
    # labextension/, see jupyterlab.outputDir in js/package.json
    # These files are copied to extensions/ipyvue-flatsurf/ in
    # JupyterLab when this package is pip-installed.
    return [{
        'src': 'labextension',
        'dest': 'ipyvue-flatsurf',
    }]


def _jupyter_nbextension_paths():
    r"""
    Called by Jupyter Notebook to find out which JavaScript assets need to be copied.
    """
    # The command `yarn build:prod` creates JavaScript assets in nbextension/.
    # These files need to be copied to the nbextensions/ipyvue-flatsurf/
    # directory in Jupyter Notebook. The entrypoint in these files is
    # extension.js.
    return [{
        'section': 'notebook',
        'src': 'nbextension',
        'dest': 'ipyvue-flatsurf',
        'require': 'ipyvue-flatsurf/extension'
    }]

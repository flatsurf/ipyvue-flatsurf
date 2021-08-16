#*********************************************************************
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
#*********************************************************************
from traitlets import Unicode
from ipywidgets import DOMWidget

class ForceLoad(DOMWidget):
    r"""
    FlatSurface includes this widget to force the `activate()` function in
    the JavaScript part of ipyvue-flatsurf to run.

    We need this to make sure that the `<flatsurf/>` component gets
    registered with Vue.js before any Vue code gets rendered by ipyvue.
    """
    _model_name = Unicode('ForceLoadModel').tag(sync=True)
    _model_module = Unicode('ipyvue-flatsurf').tag(sync=True)
    _model_module_version = Unicode('^1.0.0').tag(sync=True)

force_load = ForceLoad()

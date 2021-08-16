/*********************************************************************
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
#*********************************************************************/
import { DOMWidgetModel } from "@jupyter-widgets/base";

// This (trivial) model is used by the ForceLoad widget. The only purpose of
// that widget is to force the loading of our JavaScript assets so
// <flatsurf> gets registered with Vue.js. (A trick that we copied from
// ipyvue.)
export class ForceLoadModel extends DOMWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            _model_name: 'ForceLoadModel',
            _model_module: 'ipyvue-flatsurf',
            _model_module_version: '1.0.0',
        };
    }
}

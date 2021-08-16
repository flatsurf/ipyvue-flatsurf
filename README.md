<p align="center">
    <img alt="logo" src="https://github.com/flatsurf/ipyvue-flatsurf/raw/master/logo.svg?sanitize=true" width="300px">
</p>

<h1><p align="center">ipyvue-flatsurf</p></h1>

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL_3.0_or_later-blue.svg" alt="License: GPL 3.0 or later">
</p>

<p align="center">Jupyter Widgets for flatsurf</p>
<hr>

This project provides Jupyter Widgets for the [flatsurf suite](https://flatsurf.github.io). In particular it provides interactive widgets for translation surfaces from [sage-flatsurf](https://flatsurf.github.io/sage-flatsurf) and their quotiens and flow decompositions. Behind the scenes, this project provides the glue between the mathematical objects of [sage-flatsurf](https://flatsurf.github.io/sage-flatsurf) and [flatsurf](https://github.com/flatsurf/flatsurf) and actual visualization in the browser which is implemented in [vue-flatsurf](https://github.com/flatsurf/vue-flatsurf).

There are two related projects in this repository:
* a Python package [ipyvue-flatsurf](./ipyvue_flatsurf) and
* the [frontend glue](./js) written in JavaScript.
* the frontend glue written in JavaScript which is also called [ipyvue-flatsurf](./js).

Note that this project is in an alpha stage. The interface is mostly a proof-of-concept and very likely to change substantially in the future.

Installation
------------

If you already have [sage-flatsurf](https://github.com/flatsurf/sage-flatsurf) and [pyflatsurf](https://github.com/flatsurf/flatsurf), you can install ipyvue-flatsurf with pip:

    pip install ipyvue-flatsurf

Otherwise, we recommend to use mamba:

* Install [mambaforge](https://github.com/conda-forge/miniforge#mambaforge)
* `git clone https://github.com/flatsurf/ipyvue-flatsurf.git`
* `mamba env create -n flatsurf -f ipyvue-flatsurf/binder/environment.yml`
* `conda activate flatsurf`
* `jupyter notebook ipyvue-flatsurf/examples`

Binder
------

You can try out sage-flatsurf and ipyvue-flatsurf here: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/flatsurf/ipyvue-flatsurf/master?filepath=%2Fexamples)

Unfortunately, this environment might take quite a while to start.

Development
-----------

Install a local copy of this package:

    git clone https://github.com/flatsurf/ipyvue-flatsurf.git
    cd ipyvue-flatsurf
    pip install -e .

When working with the classical notebook:

    jupyter nbextension install --py --symlink --overwrite --sys-prefix ipyvue_flatsurf
    jupyter nbextension enable --py --sys-prefix ipyvue_flatsurf

When working with JupyterLab:

    jupyter labextension develop --overwrite ipyvue_flatsurf

To rebuild the JavaScript code after making changes to anything in the `js/`
directory:

    cd js
    yarn run build
    cd ..
    pip install -e . --no-deps # for JupyterLab

You then need to refresh the Notebook/JupyterLab page for the changes to take effect.

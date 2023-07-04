<p align="center">
    <img alt="logo" src="https://github.com/flatsurf/ipyvue-flatsurf/raw/master/logo.svg?sanitize=true" width="300px">
</p>

<h1><p align="center">ipyvue-flatsurf</p></h1>

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL_3.0_or_later-blue.svg" alt="License: GPL 3.0 or later">
  <a href="https://github.com/flatsurf/ipyvue-flatsurf/actions/workflows/test.yml"><img src="https://github.com/flatsurf/ipyvue-flatsurf/actions/workflows/test.yml/badge.svg" alt="Test"></a>
  <a href="https://doi.org/10.5281/zenodo.5208761"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.5208761.svg" alt="DOI 10.5281/zenodo.5208761"></a>
</p>

<p align="center">Jupyter Widgets for flatsurf</p>
<hr>

This project provides Jupyter Widgets for the [flatsurf suite](https://flatsurf.github.io). In particular it provides interactive widgets for surfaces from [sage-flatsurf](https://flatsurf.github.io/sage-flatsurf) and their quotients and flow decompositions. Behind the scenes, this project provides the glue between the mathematical objects of [sage-flatsurf](https://flatsurf.github.io/sage-flatsurf) and their visualization in the browser which is implemented in [vue-flatsurf](https://github.com/flatsurf/vue-flatsurf).

Note that this project is in an alpha stage. The interface is mostly a proof-of-concept and very likely to change substantially in the future.

Installation
------------

If you already have [sage-flatsurf](https://github.com/flatsurf/sage-flatsurf) and [pyflatsurf](https://github.com/flatsurf/flatsurf), you can install ipyvue-flatsurf with pip:

    pip install ipyvue-flatsurf

Otherwise, you can install the dependencies with conda. We recommend to download and install [mambaforge](https://github.com/conda-forge/miniforge#mambaforge).

    git clone https://github.com/flatsurf/ipyvue-flatsurf.git
    mamba env create -n flatsurf -f ipyvue-flatsurf/binder/environment.yml
    conda activate flatsurf
    jupyter lab ipyvue-flatsurf/examples

Binder
------

You can try out sage-flatsurf and ipyvue-flatsurf online using Binder:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/flatsurf/ipyvue-flatsurf/0.5.6?filepath=%2Fexamples)

Unfortunately, the Binder environment might take quite a while to start.

Development
-----------

Install a local copy of this package:

    git clone https://github.com/flatsurf/ipyvue-flatsurf.git
    cd ipyvue-flatsurf
    pip install -e .
    jupyter labextension develop --overwrite ipyvue_flatsurf

To use the [Vue.js
devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/), you
should also install [this
hack](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/) since
otherwise, Vue won't be detected properly.

How to Cite this Project
------------------------

If you have used this project in the preparation of a publication, please cite it as described on our [Zenodo page](https://doi.org/10.5281/zenodo.5208761).

Acknowledgements
----------------

* Julian Rüth's contributions to this project have been supported by the Simons Foundation Investigator grant of Alex Eskin.

Maintainers
-----------

* [@saraedum](https://github.com/saraedum)


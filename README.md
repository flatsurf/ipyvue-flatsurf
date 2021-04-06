ipyvue-flatsurf
==================

Visualize Flat Surfaces in Jupyter Notebooks and JupyterLab

Installation
------------

To install use pip:

    pip install ipyvue_flatsurf

Development
-----------

Install a local copy of this package:

    git clone https://github.com/saraedum/ipyvue-flatsurf.git
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
    pip install -e . --no-deps

You then need to refresh the Notebook/JupyterLab page for the changes to take effect.

# flatsurf-widgets

Jupyter Widgets for flatsurf

## Installation

Enable this extension in Jupyter Notebooks with

```bash
pip install .
```

If you use *Jupyter Lab*, you also need jupyterlab-manager and you might want to
rebuild for the new extensions to be immediately available:

```bash
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter lab build
```

## Development

Development is probably best done in a dedicated conda environment

```bash
conda create -c conda-forge -n flatsurf-widgets jupyterlab ipywidgets widgetsnbextension pip 
conda activate flatsurf-widgets
```

Install the package in develop mode (changes to the Python bits are immediately
available in the site-packages, i.e., upon next module import.) When developing
for the *classical notebook*, the non-Python part needs to be updated manually
by running this command again. However, with Hot Module Reloading (see below)
this should not be necessary unless the bootstrapping JavaScript at the bottom
changes. Since we want the examples and tests to be able to run, we also
install all extra requirements that they configure in `setup.py`.

```bash
pip install -e ".[test, examples]"
```

For the *classical notebook*, we need to make our Python package available to
the notebook

```bash
jupyter nbextension install --sys-prefix --symlink --overwrite --py flatsurf_widgets
jupyter nbextension enable --sys-prefix --py flatsurf_widgets
```

Start a *classical notebook*, and have a look at the files in `examples/`

```bash
jupyter notebook &
```

For *Jupyter Lab*, install the jupyterlab-manager and then *link* the
JavaScript bits of your extension so that Jupyter Lab automatically rebuilds
when they change.

```bash
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension link .
```

Start *Jupyter Lab* and have a look at the files in `examples/`

```bash
jupyter lab --watch &
```

If working with *Jupyter Lab*, you should also spawn `yarn run watch` so that
our JavaScript bits get rebuilt when necessary. (These rebuilds trigger a
rebuild of Jupyter Lab's bundle because we gave it the `--watch` parameter.)

When not using Hot Reloading (below) and the JavaScript code has changed, you
need to reload the browser tab for changes to take effect once the rebuild is
complete. When the Python code changes you need to restart the kernel for the
changes to take effect (shortcut <kbd>Esc</kbd><kbd>0</kbd><kbd>0</kbd>.)

### Hot Module Reloading

Assuming that you started a *classical notebook* on port 8889 as described
above, you can enable hot reloading with

```bash
yarn webpack-dev-server --config webpack-hot.config.js --hot --progress
```

Now you should be able to connect to a notebook by changing `:8889` in the URL
to `:9000`.

In this mode, changes to JavaScript should be visible (almost) immediately. For
Python changes, you still need to restart the kernel.

Unfortunately, this mode seems not to be easily possible in *Jupyter Lab* as
much of Jupyter Lab's code and extensions are bundled and then shipped to the
client as one file which makes it much harder to intercept just the bits
pertaining to this widget.

## Troubleshooting

* *Jupyter Lab* sometimes fails to realize that Java Script assets have changed
  when reinstalling with `pip install .`. In fact, `yarn` seems to pull the
  wrong package from its internal cache. This might be related to installing
  the same version of this package without creating a new commit in git. In any
  case, wiping `~/.cache/yarn` and `node_modules` in Jupyter Lab's `staging/`
  area, followed by a `jupyter lab build` seems to resolve this problem.

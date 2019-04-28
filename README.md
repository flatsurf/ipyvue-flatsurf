
# flatsurf-widgets

[![Build Status](https://travis-ci.org/flatsurf/flatsurf-widgets.svg?branch=master)](https://travis-ci.org/flatsurf/flatsurf_widgets)
[![codecov](https://codecov.io/gh/flatsurf/flatsurf-widgets/branch/master/graph/badge.svg)](https://codecov.io/gh/flatsurf/flatsurf-widgets)


Jupyter Widgets for flatsurf

## Installation

You can install using `pip`:

```bash
pip install flatsurf_widgets
```

Or if you use jupyterlab:

```bash
pip install flatsurf_widgets
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:
```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] flatsurf_widgets
```

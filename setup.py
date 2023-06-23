#*********************************************************************
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
#*********************************************************************
from __future__ import print_function
from setuptools import setup, find_packages
import os
from os.path import join as pjoin
from distutils import log

from jupyter_packaging import (
    create_cmdclass,
    install_npm,
    ensure_targets,
    combine_commands,
)


here = os.path.dirname(os.path.abspath(__file__))

log.set_verbosity(log.DEBUG)
log.info('setup.py entered')
log.info('$PATH=%s' % os.environ['PATH'])

js_dir = pjoin(here, 'js')

# Representative files that should exist after a successful build
jstargets = [
    pjoin(js_dir, 'dist', 'index.js'),
]

data_files_spec = [
    ('share/jupyter/nbextensions/ipyvue-flatsurf', 'ipyvue_flatsurf/nbextension', '*.*'),
    ('share/jupyter/labextensions/ipyvue-flatsurf', 'ipyvue_flatsurf/labextension', "**"),
    ("share/jupyter/labextensions/ipyvue-flatsurf", '.', "install.json"),
    ('etc/jupyter/nbconfig/notebook.d', '.', 'ipyvue-flatsurf.json'),
]

cmdclass = create_cmdclass('jsdeps', data_files_spec=data_files_spec)
cmdclass['jsdeps'] = combine_commands(
    install_npm(js_dir, npm=['yarn'], build_cmd='build:prod'), ensure_targets(jstargets),
)

setup_args = dict(
    name='ipyvue-flatsurf',
    version="0.5.6",
    description='Visualizations for Translations Surfaces in Jupyter Notebooks and JupyterLab',
    long_description='Visualizations for sage-flatsurf and pyflatsurf.',
    include_package_data=True,
    install_requires=[
        'ruamel.yaml>=0.17.10,<0.18',
        'sage-flatsurf>=0.5,<0.6',
        'pyflatsurf>=3.9.0,<4',
        'ipyvue-async>=0.1.0,<0.2',
        'jupyter-ui-poll>=0.2.1,<0.3',
        # We can only use versions of ipyvue that bundle the version of vue that
        # vue-flatsurf was built against. Otherwise, the compiled single file
        # components might contain render() functions that are not compatible
        # with the vue version that ipyvue bundles. (So, when upgrading this
        # pin, make sure to bump the pins in js/package.json as well
        # accordingly.)
        'ipyvue>=1.5.0,<=1.7.0',
    ],
    packages=find_packages(),
    zip_safe=False,
    cmdclass=cmdclass,
    author='Julian Rüth',
    author_email='julian.rueth@fsfe.org',
    url='https://github.com/flatsurf/ipyvue-flatsurf',
    keywords=[
        'ipython',
        'jupyter',
        'widgets',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: IPython',
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Multimedia :: Graphics',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)

setup(**setup_args)

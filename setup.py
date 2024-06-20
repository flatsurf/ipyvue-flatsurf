# ********************************************************************
#  This file is part of ipyvue-flatsurf.
#
#        Copyright (C) 2021-2023 Julian Rüth
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
from __future__ import print_function
from setuptools import setup, find_packages
import os
from distutils import log


here = os.path.dirname(os.path.abspath(__file__))

log.set_verbosity(log.DEBUG)
log.info('setup.py entered')
log.info('$PATH=%s' % os.environ['PATH'])

data_files_spec = [
    ('share/jupyter/nbextensions/ipyvue-flatsurf', 'ipyvue_flatsurf/nbextension', '*.*'),
    ('share/jupyter/labextensions/ipyvue-flatsurf', 'ipyvue_flatsurf/labextension', "**"),
    ("share/jupyter/labextensions/ipyvue-flatsurf", '.', "install.json"),
    ('etc/jupyter/nbconfig/notebook.d', '.', 'ipyvue-flatsurf.json'),
]

setup_args = dict(
    name='ipyvue-flatsurf',
    version="0.6.1",
    description='Visualizations for Translations Surfaces in Jupyter Notebooks and JupyterLab',
    long_description='Visualizations for sage-flatsurf and pyflatsurf.',
    include_package_data=True,
    install_requires=[
        'ruamel.yaml>=0.17.10,<0.18',
        'sage-flatsurf>=0.5,<0.6',
        'pyflatsurf>=3.9.0,<4',
        'jupyter-ui-poll>=0.2.1,<0.3',
        'ipymuvue>=0.3.0,<0.7.0',
    ],
    packages=find_packages(),
    zip_safe=False,
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
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)

setup(**setup_args)

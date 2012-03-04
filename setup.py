#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup

import os
import sys

kwargs = {}

try:
    import setuptools
    kwargs['use_2to3'] = True
    kwargs['test_suite'] = 'tests'
except ImportError:
    pass

base_dir = os.path.dirname(__file__)
long_description = open(os.path.join(base_dir, 'README.rst')).read()

setup(
    name = "pyroutes",
    version = "0.4.1",
    author_email = 'klette@samfundet.no',
    author = 'Kristian Klette',
    description = "A small WSGI wrapper for creating small python web apps",
    license = 'GPLv2',
    long_description = long_description,
    url = 'http://github.com/pyroutes/pyroutes',
    package_data = {'pyroutes': ['default_templates/*.xml', 'default_templates/fileserver/*.xml']},
    packages = ['pyroutes', 'pyroutes.http', 'pyroutes.template', 'pyroutes.contrib', 'pyroutes.middleware'],
    requires = ['wsgiref'],
    scripts = ['bin/pyroutes-admin.py'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
    ],
    **kwargs
)

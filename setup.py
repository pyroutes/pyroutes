#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 \
            as build_py
except ImportError:
    from distutils.command.build_py import build_py

import os

desc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name = "pyroutes",
    version = "0.4.1",
    author_email = 'klette@samfundet.no',
    author = 'Kristian Klette',
    description = "A small WSGI wrapper for creating small python web apps",
    license = 'GPLv2',
    long_description = desc,
    url = 'http://github.com/pyroutes/pyroutes',
    package_data = {'pyroutes': ['default_templates/*.xml', 'default_templates/fileserver/*.xml']},
    packages = ['pyroutes', 'pyroutes.http', 'pyroutes.template', 'pyroutes.contrib', 'pyroutes.middleware'],
    requires = ['wsgiref'],
    scripts = ['bin/pyroutes-admin.py'],
    cmdclass = {'build_py': build_py},
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
        ]

)


#!/usr/bin/env python
# coding=utf-8

import os
import sys

from distutils.core import setup, Command

sys.path.insert(0, './layout/')

import package

# try:
#     from setuptools import setup
# except ImportError, err:
#     sys.stderr.write("""
# You need to install the 'setuptools' Python package first.
# 
# You can get it from here: http://pypi.python.org/pypi/setuptools/
# 
# """)
#     sys.exit(1)

if __name__ == '__main__':
    setup(
        name='package',
        version=package.__version__,

        description='package is a package to package your package',
        long_description = open('README.rst', 'r').read(),

        # See: http://pypi.python.org/pypi?:action=list_classifiers
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python',
            'Topic :: Software Development',
            'Topic :: System :: Software Distribution',
            'Topic :: Utilities',
        ],

        author='Ingy dot Net',
        author_email='ingy@ingy.net',
        url='http://www.pypi.org/pypi/package/',

        packages=[],
#         install_requires = [
#             'setuptools',
#             'pyyaml',
#         ],
    )

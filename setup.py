#!/usr/bin/env python
# coding=utf-8

import os
import sys
import codecs
import glob

from distutils.core import Command

try:
    from setuptools import setup
except ImportError, err:
    sys.stderr.write("""
You need to install the 'setuptools' Python package first.

You can get it from here: http://pypi.python.org/pypi/setuptools/

""")
    sys.exit(1)

import package


if __name__ == '__main__':
    packages = []
    for t in os.walk('package'):
        packages.append(t[0].replace('/', '.'))

    setup(
        name='package',
        version=package.__version__,

        description='package is a package to package your package',
        long_description = codecs.open(
            os.path.join(
                os.path.dirname(__file__),
                'README.rst'
            ),
            'r',
            'utf-8'
        ).read(),

        # See: http://pypi.python.org/pypi?:action=list_classifiers
        classifiers = [
            'Development Status :: 2 - Pre-Alpha',
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
        license='Simplified BSD License',
        url='http://www.pypi.org/pypi/package/',

        packages=packages,

        install_requires = [
            'setuptools',
            'pyyaml',
        ],
    )

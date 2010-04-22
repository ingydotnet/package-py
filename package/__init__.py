"""\
package package package
"""

import os, sys

__version__ = '0.0.1'

has_setuptools = False

from package.errors import *

try:
    from setuptools import setup as real_setup
    has_setuptools = True
except ImportError, err:
    try:
        from distutils.core import setup as real_setup
    except ImportError, err:
        die(ENOSETUP)

def setup():
    if not sys.path.exists('package/info.py'):
        generate_package_info()

    try:
        import package.info
    except ImportError, err:
        die(ENOINFO)

    real_setup(**get_setup_info())

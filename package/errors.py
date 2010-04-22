"""\
This module provides package management support stuff.
"""

import sys

ENOSETUP = """
For some bizarre reason, I cannot locate your Python 'setuptools' or
'distutils' packages. Paint me pathetic, but I just cannot go on at this
point.
"""

ENOINFO = """\
I can't find the 'package.info' module. If you are the author of this package,
please run this command:

    make package/info.py

If you are just some dude installing this Python package, please write the
author an email about the missing 'package.info' module.
"""

def die(msg):
    sys.stderr.write(msg)
    sys.exit(1)

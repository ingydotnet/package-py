"""\
This module provides package management support stuff.
"""

import sys

ENONAME = """
The 'name' entry is required in your `info.yaml` file.

"""

ENOSETUP = """
For some bizarre reason, I cannot locate your Python 'setuptools' or
'distutils' packages. Paint me pathetic, but I just cannot go on at this
point.

"""

ENOINFO = """
I can't find the 'package.info' module. If you are the author of this package,
please run this command:

    make package-info

If you are simply some dude installing this Python package, please contact the
author about the missing 'package.info' module.

"""

ENOYAML = """
You need to install pyyaml to use the package-py framework as a package author.

"""

ENOLOCALINFO = """
Strange. I can't find the file called ./package/info.yaml. Did you delete it?

"""

ELOCALINFONOTSET = """
It seems like you haven't edited the ./package/info.yaml file yet. You need to
put all the pertinent information in there in order to proceed.

"""

ENOSETUPTOOLS = """
The package you are trying to install depends on an installation feature that
requires the 'setuptools' Python module, but you do not have that module
installed. You will need to install 'setuptools' before proceeding with this
install.

You can find setuptools here:

    http://pypi.python.org/pypi/setuptools/

"""

EBADINFO = """
It seems like some of your package/info.yaml settings are wrong.
Check that file and try again. Your exception msg was:

%(err)s
"""

def die(msg, err=''):
    sys.stderr.write(msg % locals())
    sys.exit(1)

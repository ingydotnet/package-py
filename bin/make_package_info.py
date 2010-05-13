"""
This script generates a Python module called 'package.info' based on settings
in configuration files.
"""

import os, sys, pprint

sys.path.insert(0, '')

from package.errors import *

try:
    import yaml
except ImportError, err:
    die(ENOYAML)

def check_config(config):
    # require 'name'
    if 'name' not in config:
        die(ENONAME)

    # set default for version
    if not ('version' in config or
            'version_from_module' in config):
        config['version_from_module'] = config['name']

    # set default for long_description
    if not ('long_description' in config or
            'long_description_from' in config):
        import glob
        readme = glob.glob('README*')
        if readme:
            config['long_description_from'] = readme[0]

    # set default for packages
    if not ('py_modules' in config or
            'packages' in config or
            'packages_from' in config):
        config['packages_from'] = config['name']

    # get version from module
    if 'version_from_module' in config:
        module = config['version_from_module']
        del config['version_from_module']
        ns = {}
        exec('import ' + module) in ns
        config['version'] = ns[module].__version__

    # read long description
    if 'long_description_from' in config:
        file = config['long_description_from']
        del config['long_description_from']
        config['long_description'] = open(file, 'r').read()

    # find module packages
    if config.get('packages_from'):
        dirs = config['packages_from']
        del config['packages_from']
        config['packages'] = []
        for dir in dirs:
            for t in os.walk(dir):
                config['packages'].append(t[0].replace('/', '.'))

if __name__ == '__main__':
    home = os.environ.get('HOME')
    if not home:
        die(ENOHOME)

    config = {}

    f = home + '/.package-py/info.yaml'
    if not os.path.exists(f):
        die(ENOHOMEINFO)
    d = yaml.load(open(f, 'r'))
    config.update(d)

    f = './package/info.yaml'
    if not os.path.exists(f):
        die(ENOLOCALINFO)
    d = yaml.load(open(f, 'r'))
    if not d.get('name'):
        die(ELOCALINFONOTSET)
    config.update(d)

    check_config(config)

    dict = pprint.pformat(config, indent=2)

    module = """\
def get():
    dict = {}
    dict.update(
%(dict)s
)
    return dict
""" % locals()
    
    f = open('package/info.py', 'w')
    f.write(module)
    f.close()

    print "Created the 'package/info.py' module for this package."

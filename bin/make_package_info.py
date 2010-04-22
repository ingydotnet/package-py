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
    if config.get('version_from_module'):
        module = config['version_from_module']
        del config['version_from_module']
        ns = {}
        exec('import ' + module) in ns
        config['version'] = ns[module].__version__
    if config.get('long_description_from'):
        file = config['long_description_from']
        del config['long_description_from']
        config['description'] = open(file, 'r').read()
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

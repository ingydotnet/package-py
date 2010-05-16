"""
This script generates a Python module called 'package.info' based on settings
in configuration files.
"""

import os, sys, pprint, glob

sys.path.insert(0, '')

from package.errors import *

try:
    import yaml
except ImportError, err:
    die(ENOYAML)

def check_config(config):
    # require 'name'
    if ('name' not in config or
            config['name'] == 'your-package'):
        die(ELOCALINFONOTSET)

    # set default for version
    if not ('version' in config or
            'version_from_module' in config):
        config['version_from_module'] = config['name']

    # set default for long_description
    if not ('long_description' in config or
            'long_description_from' in config):
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

    if 'description' not in config:
        module = config['name']
        ns = {}
        exec('import ' + module) in ns
        config['description'] = ns[module].__doc__

    # read long description
    if 'long_description_from' in config:
        file = config['long_description_from']
        del config['long_description_from']
        config['long_description'] = open(file, 'r').read()

    # find module packages
    if 'packages_from' in config:
        dirs = config['packages_from']
        del config['packages_from']
        config['packages'] = []
        for dir in dirs:
            for t in os.walk(dir):
                config['packages'].append(t[0].replace('/', '.'))

    if 'scripts' not in config:
        config['scripts'] = glob.glob('bin/*')

if __name__ == '__main__':
    home = os.environ.get('HOME')
    if not home:
        die(ENOHOME)

    config = {}

    f = './package/info.yaml'
    if not os.path.exists(f):
        die(ENOLOCALINFO)
    d = yaml.load(open(f, 'r'))

    if 'include' in d:
        config.update(yaml.load(open(d['include'], 'r')))
        del d['include']

    config.update(d)

    if (os.path.exists('your-package') and
            'name' in config and
            config['name'] != 'your-package'):
        os.rename('your-package', config['name'])

    check_config(config)

    info = pprint.pformat(config, indent=2)

    module = """\
def get():
    info = {}
    info.update(
%(info)s
)
    return info
""" % locals()
    
    f = open('package/info.py', 'w')
    f.write(module)
    f.close()

    print "Created the 'package/info.py' module for this package."

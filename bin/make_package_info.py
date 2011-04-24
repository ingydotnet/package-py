"""
This script generates a Python module called 'package.info' based on settings
in configuration files.
"""

import os, sys, re, pprint, glob, datetime

sys.path.insert(0, '')

from package.errors import *

try:
    import yaml
except ImportError, err:
    die(ENOYAML)

def get_config():
    config = {
        'current_year': datetime.date.today().year,
        'time_string': os.popen('date').read().rstrip(),
    }

    f = './package/info.yaml'
    if not os.path.exists(f):
        die(ENOLOCALINFO)
    d = yaml.load(open(f, 'r'))

    if 'include' in d:
        config.update(yaml.load(open(d['include'], 'r')))
        del d['include']

    config.update(d)
    return config

def check_name(config):
    # require 'name'
    if ('name' not in config or
            config['name'] == 'yourpackage'):
        die(ELOCALINFONOTSET)

def check_config(config):
    # Remove non-standard keys
    del config['current_year']
    del config['time_string']
    del config['github_id']

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
        config['packages_from'] = [ config['name'] ]

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
        desc = ns[module].__doc__
        m = re.match(r'\s*([^\.\!\n]*)', desc)
        if m:
            config['description'] = m.groups()[0]

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

def write_info_py(config):
    info = pprint.pformat(config, indent=2)

    module = """\
def get():
    info = {}
    info.update(
%(info)s
)
    return info
""" % locals()

    file = 'package/info.py'
    action = os.path.exists(file) and 'Updated' or 'Created'
    print "%(action)s the '%(file)s' module for this package." % locals()
    
    f = open(file, 'w')
    f.write(module)
    f.close()

def update_template(config, file):
    if not os.path.exists(file):
        print "Warning: %s does not exist." % file
        return
    f = open(file, 'r')
    text = f.read()
    f.close()
    if not re.search(r'%\(\w+\)s', text):
        return
    try:
        text = text % config
    except KeyError, err:
        die(EBADINFO, err=err)
    f = open(file, 'w')
    f.write(text)
    f.close()
    print "Updated '%s' with your info" % file

def add_failing_tests(config):
    file = "%s/__init__.py" % config['name']
    f = open(file, 'r')
    text = f.read()
    f.close

    text = re.sub(r'# raise ', 'raise ', text)
    f = open(file, 'w')
    f.write(text)
    f.close


if __name__ == '__main__':
    config = get_config()

    initial_setup = False
    if (os.path.exists('yourpackage') and
            'name' in config and
            config['name'] != 'yourpackage'):
        os.rename('yourpackage', config['name'])
        initial_setup = True

    check_name(config)
    update_template(config, 'CHANGES.yaml')
    update_template(config, 'tests/test_import.py')
    update_template(config, 'LICENSE')
    # XXX temporary hack, until template IF works
    config['github_id'] = config.get('github_id', 'your-github-id')
    update_template(config, 'README.rst')
    update_template(config, "%s/__init__.py" % config['name'])
    check_config(config)
    write_info_py(config)
    update_template(config, 'package/info.py')
    if initial_setup:
        add_failing_tests(config)

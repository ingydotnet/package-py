"""
This script tweaks the Makefile a little bit after it is copied from
package-py.
"""

import sys, re

if __name__ == '__main__':
    f = open('Makefile', 'r')
    text = f.read()
    f.close()

    base = sys.argv[1]

    text = re.compile(
        r'^setup:\s', re.MULTILINE
    ).sub(
        '# setup: ',
        text
    )

    text = re.compile(
        r'^PACKAGE_BASE\s+=\s+.*', re.MULTILINE
    ).sub(
        'PACKAGE_BASE = %s' % base,
        text
    )

    f = open('Makefile', 'w')
    f.write(text)
    f.close()

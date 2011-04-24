This document describes the design goals and details of `package`, the package
package package.

Glossary
--------

author
    A person who writes and distributes Python packages.

package
    `package` has a double meaning in Python. It means either `namespace` or
    `distribution`. In this text, it means the latter.

user
    A person who installs and uses Python packages.

Design Goals
------------

* Give authors a simple way to start new packages.
* Put all the author/package info in a yaml file. (instead of `setup.py`)
* Lead users through the installation matrix with lots of helpful suggestions.
* Provide authors with a set of simple standards for various author tasks.
* Provide an easy upgrade path for new releases of package-py.

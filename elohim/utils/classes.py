#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A handful of utility functions and classes for manipulating
python classes, using python's reflection
"""

import pkgutil


def import_modules(path, module):
    for _f, submodule, _i in pkgutil.walk_packages(path,
            '{module}.'.format(module=module)):
        __import__(submodule)

def list_subclasses(cls, module, path):
    """find all subclasses of a classe, given a module where they
    are stored

    :param cls: base class which subclasses must be found
    :param module: base module of all subclasses
    :param path: folder to the subclasses location
    :returns: a set of the given class's subclasses
    """

    def find_subclasses(cls, seen):
        """recursive method to iterates through subclasses

        :param seen: already found classes. Found classes will be added
            to this list
        """
        try:
            subs = cls.__class__.__subclasses__()
        except TypeError:
            subs = cls.__class__.__subclasses__(cls)
        for sub in subs:
            seen.add(sub)
            find_subclasses(sub, seen)

    import_modules(path, module)

    result = set()
    find_subclasses(cls, result)
    return result


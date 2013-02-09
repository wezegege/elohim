#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pkgutil


def list_subclasses(cls, module, path):
    for _f, submodule, _i in pkgutil.walk_packages(path,
            '{module}.'.format(module=module)):
        __import__(submodule)
    result = set()
    find_subclasses(cls, result)
    return result


def find_subclasses(cls, seen):
    try:
        subs = cls.__class__.__subclasses__()
    except TypeError:
        subs = cls.__class__.__subclasses__(cls)
    for sub in subs:
        seen.add(sub)
        find_subclasses(sub, seen)

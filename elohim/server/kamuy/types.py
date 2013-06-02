#!/usr/bin/env python
# -*- coding: utf-8 -*-


from elohim.utils import plugin

namespace = plugin.Namespace()


@namespace.entity('type')
class Type(object):
    pass


@namespace.entity('list')
class List(Type):
    def __init__(self, subtype):
        self.subtype = subtype


@namespace.entity('condition')
class Condition(Type):
    pass

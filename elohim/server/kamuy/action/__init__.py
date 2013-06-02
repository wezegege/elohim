#!/usr/bin/env python
# -*- coding: utf-8 -*-


from elohim.utils import plugin

namespace = plugin.Namespace()


@namespace.entity('action')
class Action(object):
    pass


def entry_point(func):
    return func


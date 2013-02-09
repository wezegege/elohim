#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.utils import classes
from elohim import action

import collections


class Client(action.Entity):
    @classmethod
    def list_clients(cls):
        subs = classes.list_subclasses(cls, __name__, __path__)
        result = collections.defaultdict(dict)
        for sub in subs:
            result[sub.type][sub.name] = sub
        return result


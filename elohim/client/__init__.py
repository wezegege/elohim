#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Set of clients for a turn based rules engine game
"""

from elohim.utils import classes
from elohim import action
from elohim.action import parameter

import collections


class Client(action.Entity):
    """Base class for a client, which must define default interface to
    communicate with the server
    """
    parameters = [
            ('name', parameter.ValueParameter()),
            ]

    @classmethod
    def list_clients(cls):
        """Look for installed clients
        """
        subs = classes.list_subclasses(cls, __name__, __path__)
        result = collections.defaultdict(dict)
        for sub in subs:
            result[sub.type][sub.name] = sub
        return result


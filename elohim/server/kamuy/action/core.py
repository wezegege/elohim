#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kamuy import types, action

namespace = action.namespace.namespace(__name__)


@namespace.entity('check-condition')
class CheckCondition(action.Action):
    parameters = [
            ('conditions', types.List(types.Condition())),
            ]

    @utils.entry_point
    def play():
        pass

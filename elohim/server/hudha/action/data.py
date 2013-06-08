#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Data tree manipulation actions
"""

from elohim import action
from elohim.action import parameter


namespace = action.action.namespace(__name__)


@namespace.entity('transfer-current')
class TransferCurrent(action.Action):
    """Transfer value of a field to another, and reset it
    """
    parameters = [
            ('origin', parameter.PlayerData()),
            ('destination', parameter.PlayerData()),
            ]

    def play(self):
        origin = ['players', 'current'] + self.values['origin']
        destination = ['players', 'current'] + self.values['destination']
        self.data.add(destination, self.data.get(origin))
        self.data.reset(origin)


@namespace.entity('set-current')
class SetCurrent(action.Action):
    """Set given field to current player
    """
    parameters = [
            ('variable', parameter.PlayerData()),
            ('value', parameter.ValueParameter()),
            ]

    def play(self):
        variable = ['players', 'current'] + self.values['variable']
        self.data.set(variable, self.values['value'])


@namespace.entity('while-current-true')
class WhileCurrentTrue(action.Action):
    """Launch actions until a criteria evaluates as false
    """
    parameters = [
            ('variable', parameter.PlayerData()),
            ('actions', parameter.ActionList()),
            ]

    def play(self):
        variable = ['players', 'current'] + self.values['variable']
        self.data.set(variable, True)
        while self.data.get(variable):
            self.send('round')
            for todo in self.values['actions']:
                todo.play()

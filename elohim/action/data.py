#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.engine.data import Data
from elohim.action import GameFabric


library = GameFabric.make_library('data')


@library('transfer-current')
class TransferCurrent(object):
    def __init__(self, origin, destination, reset=0):
        self.origin = origin
        self.destination = destination
        self.reset = reset

    def player_data(self):
        return [(self.origin, self.reset),
                (self.destination, self.reset)]

    def play(self):
        Data.add(['players', 'current'] + self.destination, Data.get(['players', 'current'] + self.origin))
        Data.set(['players', 'current'] + self.origin, self.reset)


@library('set-current')
class SetCurrent(object):
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def player_data(self):
        return [(self.variable, None)]

    def play(self):
        Data.set(['players', 'current'] + self.variable, self.value)


@library('while-current-true')
class WhileCurrentTrue(object):
    def __init__(self, variable, actions):
        self.variable = variable
        self.actions = actions

    def player_data(self):
        result = [(self.variable, False)]
        for action in self.actions:
            result.extend(action.player_data())
        return result

    def play(self):
        Data.set(['players', 'current'] + self.variable, True)
        while Data.get(['players', 'current'] + self.variable):
            Data.get(['players', 'current', 'client']).send('round')
            for action in self.actions:
                action.play()

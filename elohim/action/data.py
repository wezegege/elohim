#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim import action
from elohim.action import parameter


class TransferCurrent(action.Action):
    library = 'data'
    name = 'tranfer-current'
    parameters = [
            ('origin', parameter.PlayerData()),
            ('destination', parameter.PlayerData()),
            ]

    def play(self):
        origin = ['players', 'current'] + self.values['origin']
        destination = ['players', 'current'] + self.values['destination']
        self.data.add(destination, self.data.get(origin))
        self.data.reset(origin)


class SetCurrent(action.Action):
    library = 'data'
    name = 'set-current'
    parameters = [
            ('variable', parameter.PlayerData()),
            ('value', parameter.ValueParameter()),
            ]

    def play(self):
        variable = ['players', 'current'] + self.values['variable']
        self.data.set(variable, self.values['value'])


class WhileCurrentTrue(action.Action):
    library = 'data'
    name = 'while-current-true'
    parameters = [
            ('variable', parameter.PlayerData()),
            ('actions', parameter.ActionList()),
            ]

    def play(self):
        variable = ['players', 'current'] + self.values['variable']
        self.data.set(variable, True)
        while self.data.get(variable):
            self.send('round')
            for action in self.values['actions']:
                action.play()

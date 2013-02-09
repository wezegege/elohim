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
        self.data.add(['players', 'current'] + self.values['destination'],
                self.data.get(['players', 'current'] + self.values['origin']))
        self.data.set(['players', 'current'] + self.values['origin'], 0)


class SetCurrent(action.Action):
    library = 'data'
    name = 'set-current'
    parameters = [
            ('variable', parameter.PlayerData()),
            ('value', parameter.ValueParameter()),
            ]

    def play(self):
        self.data.set(['players', 'current'] + self.values['variable'],
                self.values['value'])


class WhileCurrentTrue(action.Action):
    library = 'data'
    name = 'while-current-true'
    parameters = [
            ('variable', parameter.PlayerData()),
            ('actions', parameter.ActionList()),
            ]

    def play(self):
        self.data.set(['players', 'current'] + self.values['variable'], True)
        while self.data.get(['players', 'current'] + self.values['variable']):
            self.data.get(['players', 'current', 'client']).send('round')
            for action in self.values['actions']:
                action.play()

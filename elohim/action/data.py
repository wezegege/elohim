#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.action import Action
from elohim.action.parameter import PlayerData, ValueParameter, ActionList


class TransferCurrent(Action):
    library = 'data'
    name = 'tranfer-current'
    parameters = [
            ('origin', PlayerData()),
            ('destination', PlayerData()),
            ]

    def play(self):
        self.data.add(['players', 'current'] + self.values['destination'],
                self.data.get(['players', 'current'] + self.values['origin']))
        self.data.set(['players', 'current'] + self.values['origin'], 0)


class SetCurrent(Action):
    library = 'data'
    name = 'set-current'
    parameters = [
            ('variable', PlayerData()),
            ('value', ValueParameter()),
            ]

    def play(self):
        self.data.set(['players', 'current'] + self.values['variable'],
                self.values['value'])


class WhileCurrentTrue(Action):
    library = 'data'
    name = 'while-current-true'
    parameters = [
            ('variable', PlayerData()),
            ('actions', ActionList()),
            ]

    def play(self):
        self.data.set(['players', 'current'] + self.values['variable'], True)
        while self.data.get(['players', 'current'] + self.values['variable']):
            self.data.get(['players', 'current', 'client']).send('round')
            for action in self.values['actions']:
                action.play()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.action import Action


class TransferCurrent(Action):
    library = 'data'
    name = 'tranfer-current'
    parameters = [
            ('origin', 'player_data'),
            ('destination', 'player_data'),
            ]

    def play(self):
        self.data.add(['players', 'current'] + self.values['destination'],
                self.data.get(['players', 'current'] + self.values['origin']))
        self.data.set(['players', 'current'] + self.values['origin'], 0)


class SetCurrent(Action):
    library = 'data'
    name = 'set-current'
    parameters = [
            ('variable', 'player_data'),
            ('value', 'value'),
            ]

    def play(self):
        self.data.set(['players', 'current'] + self.values['variable'],
                self.values['value'])


class WhileCurrentTrue(Action):
    library = 'data'
    name = 'while-current-true'
    parameters = [
            ('variable', 'player_data'),
            ('actions', 'actions'),
            ]

    def play(self):
        self.data.set(['players', 'current'] + self.values['variable'], True)
        while self.data.get(['players', 'current'] + self.values['variable']):
            self.data.get(['players', 'current', 'client']).send('round')
            for action in self.values['actions']:
                action.play()

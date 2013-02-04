#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.action import Action
from elohim.action.parameter import PlayerData, ConditionParameter, ActionList


class SetWinner(Action):
    library = 'core'
    name = 'set-winner'
    parameters = [
        ('criteria', PlayerData()),
        ]

    def play(self):
        name = None
        score = None
        for player in self.data.get(['players', 'list']):
            if score is None or \
                    score < self.data.get(self.values['criteria'], player):
                score = self.data.get(self.values['criteria'], player)
                name = player['name']
        for player in self.data.get(['players', 'list']):
            player['client'].send('winner', name=name)


class If(Action):
    library = 'core'
    name = 'if'
    parameters = [
        ('condition', ConditionParameter()),
        ('iftrue', ActionList()),
        ('iffalse', ActionList()),
        ]

    def play(self):
        if self.values['condition'].evaluate():
            for action in self.values['iftrue']:
                action.play()
        else:
            for action in self.values['iffalse']:
                action.play()


class ForeachWhile(Action):
    library = 'core'
    name = 'foreach-while'
    parameters = [
        ('condition', ConditionParameter()),
        ('actions', ActionList()),
        ]

    def play(self):
        while self.values['condition'].evaluate():
            while True:
                self.data.set(['players', 'index'],
                        (self.data.get(['players', 'index']) + 1) %
                        self.data.get(['players', 'count']))
                if self.data.get(['players', 'list',
                        self.data.get(['players', 'index']), 'ingame']):
                    break
            self.data.set(['players', 'current'],
                    self.data.get(['players', 'list', self.data.get(['players', 'index'])]))

            self.data.get(['players', 'current', 'client']).send('playerturn')
            for action in self.values['actions']:
                action.play()


class Sequence(Action):
    library = 'core'
    name = 'sequence'
    parameters = [
            ('actions', ActionList()),
            ]

    def play(self):
        for action in self.values['actions']:
            action.play()

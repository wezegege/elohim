#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim import action
from elohim.action import parameter


class SetWinner(action.Action):
    library = 'core'
    name = 'set-winner'
    parameters = [
        ('criteria', parameter.PlayerData()),
        ]

    def play(self):
        name = None
        score = None
        for player in self.data.get(['players', 'list']):
            if score is None or score < player.get(self.values['criteria']):
                score = player.get(self.values['criteria'])
                name = player.get(['name'])
        self.send('winner', name=name)


class If(action.Action):
    library = 'core'
    name = 'if'
    parameters = [
        ('condition', parameter.ConditionParameter()),
        ('iftrue', parameter.ActionList()),
        ('iffalse', parameter.ActionList()),
        ]

    def play(self):
        if self.values['condition'].evaluate():
            for todo in self.values['iftrue']:
                todo.play()
        else:
            for todo in self.values['iffalse']:
                todo.play()


class ForeachWhile(action.Action):
    library = 'core'
    name = 'foreach-while'
    parameters = [
        ('condition', parameter.ConditionParameter()),
        ('actions', parameter.ActionList()),
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

            self.send('playerturn')
            for todo in self.values['actions']:
                todo.play()


class Sequence(action.Action):
    library = 'core'
    name = 'sequence'
    parameters = [
            ('actions', parameter.ActionList()),
            ]

    def play(self):
        for todo in self.values['actions']:
            todo.play()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Core actions for most games
"""

from elohim import action
from elohim.action import parameter


namespace = action.action.namespace(__name__)


@namespace.entity('set-winner')
class SetWinner(action.Action):
    """Determine the winner through some criteria
    """
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


@namespace.entity('if')
class If(action.Action):
    """Launch actions depending on a condition evaluation
    """
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


@namespace.entity('foreach-while')
class ForeachWhile(action.Action):
    """Iterate through players until a condition is met
    """
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


@namespace.entity('sequence')
class Sequence(action.Action):
    """List of action to run sequentially
    """
    parameters = [
            ('actions', parameter.ActionList()),
            ]

    def play(self):
        for todo in self.values['actions']:
            todo.play()

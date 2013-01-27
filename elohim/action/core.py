#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.engine.data import Data


class SetWinner(object):
    def __init__(self, criteria):
        self.criteria = criteria

    def player_data(self):
        return [(self.criteria, 0)]

    def play(self):
        name = None
        score = None
        for player in Data.get(['players', 'list']):
            if score is None or score < player['score']['permanent']:
                score = player['score']['permanent']
                name = player['name']
        for player in Data.get(['players', 'list']):
            player['client'].send('winner', name=name)


class If(object):
    def __init__(self, condition, iftrue, iffalse=None):
        self.condition = condition
        self.iftrue = iftrue
        self.iffalse = list() if iffalse is None else iffalse

    def player_data(self):
        result = self.condition.player_data()
        for action in self.iftrue + self.iffalse:
            result.extend(action.player_data())
        return result

    def play(self):
        if self.condition.evaluate():
            for action in self.iftrue:
                action.play()
        else:
            for action in self.iffalse:
                action.play()


class ForeachWhile(object):
    def __init__(self, condition, actions):
        self.condition = condition
        self.actions = actions

    def player_data(self):
        result = self.condition.player_data()
        for action in self.actions:
            result.extend(action.player_data())
        return result

    def play(self):
        while self.condition.evaluate():
            while True:
                Data.set(['players', 'index'], (Data.get(['players', 'index']) + 1) % Data.get(['players', 'count']))
                if Data.get(['players', 'list', Data.get(['players', 'index']), 'ingame']):
                    break
            Data.set(['players', 'current'], Data.get(['players', 'list', Data.get(['players', 'index'])]))

            Data.get(['players', 'current', 'client']).send('playerturn')
            for action in self.actions:
                action.play()


class Sequence(object):
    def __init__(self, actions):
        self.actions = actions

    def player_data(self):
        result = list()
        for action in self.actions:
            result.extend(action.player_data())
        return result

    def play(self):
        for action in self.actions:
            action.play()

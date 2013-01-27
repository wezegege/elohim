#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.engine.data import Data


class AboveCondition(object):
    def player_data(self):
        return [(['score', 'permanent'], 0),
                (['score', 'temporary'], 0)]

    def evaluate(self):
        return Data.get(['players', 'current', 'score', 'permanent']) + Data.get(['players', 'current', 'score', 'temporary']) >= 100


class MoveCondition(object):
    def player_data(self):
        return [(['move'], None)]

    def evaluate(self):
        return Data.get(['players', 'current', 'move']) == 'roll'


class DiceCondition(object):
    def player_data(self):
        return [(['roll', 'dice'], 0)]

    def evaluate(self):
        return Data.get(['players', 'current', 'roll', 'dice']) == 1


class PlayerCondition(object):
    def player_data(self):
        return [(['score', 'permanent'], 0)]

    def evaluate(self):
        return all(player['score']['permanent'] < 100 for player in Data.get(['players', 'list']))


#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.engine import data
from elohim.bot.utils import markov
from elohim import settings

import os.path
import random


class RandomBot(object):
    def send(self, message, **kwargs):
        if message == 'askcurrent':
            self.askplayer(kwargs['destination'], kwargs['options'])

    def askplayer(self, destination, options):
        result = random.choice(list(options.keys()))
        data.Data.set(['players', 'current'] + destination, result)


class TurnTotalBot(RandomBot):
    def __init__(self, turntotal=None, wrong=1, dice=6, goal=100):
        self.turntotal = int(dice*(dice+1)/ 2 - wrong) if turntotal is None else turntotal
        self.goal = goal

    def askplayer(self, destination, options):
        actual = data.Data.get(['players', 'current', 'score', 'temporary'])
        score = data.Data.get(['players', 'current', 'score', 'permanent'])
        if actual + score > self.goal or actual >= self.turntotal:
            result = 'hold'
        else:
            result = 'roll'
        data.Data.set(['players', 'current'] + destination, result)


class PigBot(RandomBot):
    def __init__(self, dice=6, goal=100, wrong=None):
        self.dice = dice
        self.goal = goal
        self.wrong = [1] if wrong is None else wrong
        self.filename = 'pig_d{dice}w{wrong}g{goal}.txt'.format(dice=dice, goal=goal, wrong='-'.join(str(value) for value in self.wrong))
        self.filename = os.path.join(
                settings.DATAPATH,
                'games',
                'pig',
                'bot',
                self.filename)
        self.todo = list()
        try:
            with open(self.filename, 'r') as content:
                for line in content:
                    self.todo.append([int(value) for value in line.split('\t')])
        except FileNotFoundError:
            pass

    def askplayer(self, destination, options):
        current = data.Data.get(['players', 'current'])
        players = data.Data.get(['players', 'list'])

        score = current['score']['permanent']
        try:
            against = max(player['score']['permanent'] for player in players if player != current)
        except ValueError:
            against = 0
        threshold = self.todo[score][against]

        turn = current['score']['temporary']
        result = 'roll' if threshold > turn else 'hold'
        data.Data.set(['players', 'current'] + destination, result)

    def optimal(self, epsilon=10**-9):
        def pwin(p, i, j, k):
            if i + k >= self.goal:
                return 1.0
            elif j >= self.goal:
                return 0.0
            else:
                return p[i][j][k]

        def action_probs(indexes, p):
            roll = 0.0
            i, j, k = indexes
            for value in range(1, self.dice + 1):
                if value in self.wrong:
                    roll += (1.0 - pwin(p, j, i, 0))
                else:
                    roll += pwin(p, i, j, k + value)
            roll /= self.dice
            return [
                    (True, roll),
                    (False, 1 - pwin(p, j, i + k, 0)),
                    ]

        values = markov.value_iteration([
            lambda : self.goal,
            lambda i : self.goal,
            lambda i, j : self.goal - i,
            ], epsilon, action_probs, True)

        result = list()

        for i in range(self.goal):
            result.append(list())
            for j in range(self.goal):
                try:
                    todo = min(k for k in range(self.goal) if not values[i][j][k])
                    result[i].append(todo)
                except ValueError:
                    result[i].append(self.goal)

        return result

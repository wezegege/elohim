#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.client import bot
from elohim.client.bot.utils import markov
from elohim.action import parameter
from elohim import settings

import os.path
import random


class RandomBot(bot.Bot):
    name = 'random-bot'
    library = 'pig'

    def send(self, message, **kwargs):
        if message == 'askcurrent':
            current = self.data.get(['players', 'current', 'name'])
            if current == self.values['name']:
                return self.askplayer(kwargs['options'])

    def askplayer(self, options):
        result = random.choice(list(options.keys()))
        return result


class TurnTotalBot(RandomBot):
    name = 'turn-total-bot'
    library = 'pig'
    parameters = [
            ('turntotal', parameter.IntegerParameter(
                mini=1, maxi=100, mandatory=False)),
            ]

    def askplayer(self, options):
        if not self.values['turntotal']:
            dice = self.data.get(['dice', 'size'])
            wrong = self.data.get(['dice', 'wrong'])
            self.values['turntotal'] = int(dice*(dice+1)/ 2 -
                    sum(wrong))
        actual = self.data.get(['players', 'current', 'score', 'temporary'])
        score = self.data.get(['players', 'current', 'score', 'permanent'])
        if actual + score > self.data.get(['goal']) or actual >= self.values['turntotal']:
            result = 'hold'
        else:
            result = 'roll'
        return result


class PigBot(RandomBot):
    name = 'pig-bot'
    library = 'pig'

    def askplayer(self, options):
        if not 'todo' in self.values:
            filename = 'pig_d{dice}w{wrong}g{goal}.txt'.format(
                    dice=self.data.get(['dice', 'size']),
                    goal=self.data.get(['goal']),
                    wrong='-'.join(str(side)
                        for side in self.data.get(['dice', 'wrong'])))
            filename = os.path.join(
                    settings.DATAPATH,
                    'games',
                    'pig',
                    'bot',
                    filename)
            todo = list()
            try:
                with open(filename, 'r') as content:
                    for line in content:
                        todo.append([int(value) for value in line.split('\t')])
            except FileNotFoundError:
                pass
            self.values['todo'] = todo
        current = self.data.get(['players', 'current'])
        players = self.data.get(['players', 'list'])

        score = current.get(['score', 'permanent'])
        try:
            against = max(player.get(['score', 'permanent']) for player in players if player != current)
        except ValueError:
            against = 0
        threshold = self.values['todo'][score][against]

        turn = current.get(['score', 'temporary'])
        result = 'roll' if threshold > turn else 'hold'
        return result

    def optimal(self, epsilon=10**-9):
        goal = self.values['goal']

        def pwin(p, i, j, k):
            if i + k >= goal:
                return 1.0
            elif j >= goal:
                return 0.0
            else:
                return p[i][j][k]

        def action_probs(indexes, p):
            roll = 0.0
            i, j, k = indexes
            for value in range(1, self.values['dice'] + 1):
                if value in self.wrong:
                    roll += (1.0 - pwin(p, j, i, 0))
                else:
                    roll += pwin(p, i, j, k + value)
            roll /= self.values['dice']
            return [
                    (True, roll),
                    (False, 1 - pwin(p, j, i + k, 0)),
                    ]

        values = markov.value_iteration([
            lambda : goal,
            lambda i : goal,
            lambda i, j : goal - i,
            ], epsilon, action_probs, True)

        result = list()

        for i in range(goal):
            result.append(list())
            for j in range(goal):
                try:
                    todo = min(k for k in range(goal) if not values[i][j][k])
                    result[i].append(todo)
                except ValueError:
                    result[i].append(goal)

        return result

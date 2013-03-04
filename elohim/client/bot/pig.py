#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Some bot client for the dice game pig
"""

from elohim.client import bot
from elohim.client.bot.utils import markov
from elohim.action import parameter
from elohim import settings

import os.path
import random


class RandomBot(bot.Bot):
    """Bot which plays randomly the game pig
    """
    name = 'random-bot'
    library = 'pig'

    def askplayer(self, options):
        """Receive a server question and answer randomly
        """
        result = random.choice(list(options.keys()))
        return result


class TurnTotalBot(bot.Bot):
    """Bot which will aim for a certain score each turn before holding
    """
    name = 'turn-total-bot'
    library = 'pig'
    parameters = [
            ('turntotal', parameter.IntegerParameter(
                mini=1, maxi=100, mandatory=False)),
            ]

    def askplayer(self, _options):
        """Roll while the turn total is below given threshold
        """
        if not self.values['turntotal']:
            dice = self.data.get(['dice', 'size'])
            wrong = self.data.get(['dice', 'wrong'])
            self.values['turntotal'] = int(dice*(dice+1)/ 2 -
                    sum(wrong))
        actual = self.data.get(['players', 'current', 'score', 'temporary'])
        score = self.data.get(['players', 'current', 'score', 'permanent'])
        if (actual + score > self.data.get(['goal']) or
                actual >= self.values['turntotal']):
            result = 'hold'
        else:
            result = 'roll'
        return result


class PigBot(RandomBot):
    """Advanced pig bot based on game theory
    """
    name = 'pig-bot'
    library = 'pig'

    def askplayer(self, options):
        """Will play optimal game given the markov process applied to the
        pig game
        """
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
            except IOError:
                pass
            self.values['todo'] = todo
        current = self.data.get(['players', 'current'])
        players = self.data.get(['players', 'list'])

        score = current.get(['score', 'permanent'])
        try:
            against = max(player.get(['score', 'permanent'])
                    for player in players if player != current)
        except ValueError:
            against = 0
        threshold = self.values['todo'][score][against]

        turn = current.get(['score', 'temporary'])
        result = 'roll' if threshold > turn else 'hold'
        return result

    def optimal(self, epsilon=10**-9):
        """Compute optimal play for pig game
        """
        goal = self.values['goal']

        def pwin(probabilities, i, j, k):
            """Probability of winning for a given situation
            """
            if i + k >= goal:
                return 1.0
            elif j >= goal:
                return 0.0
            else:
                return probabilities[i][j][k]

        def action_probs(indexes, probabilities):
            """Compute the probability of winning for the different
            possibles actions
            """
            roll = 0.0
            i, j, k = indexes
            wrong = self.data.get(['dice', 'wrong'])
            for value in range(1, self.values['dice'] + 1):
                if value in wrong:
                    roll += (1.0 - pwin(probabilities, j, i, 0))
                else:
                    roll += pwin(probabilities, i, j, k + value)
            roll /= self.values['dice']
            return [
                    (True, roll),
                    (False, 1 - pwin(probabilities, j, i + k, 0)),
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

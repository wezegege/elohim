#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Some bots for the game hog
"""

from elohim.client.bot import pig
from elohim.client.bot.utils import markov, dices
from elohim import settings

import os.path


class HogBot(pig.RandomBot):
    """Optimal bot using markov process to determine optimal play
    """
    name = 'hog-bot'
    library = 'pig'

    def __init__(self, dice=6, goal=100, wrong=None):
        super(HogBot, self).__init__()
        self.dice = dice
        self.goal = goal
        self.wrong = [1] if wrong is None else wrong
        self.filename = 'hog_d{dice}w{wrong}g{goal}.txt'
        self.filename = self.filename.format(dice=dice, goal=goal,
                wrong='-'.join(str(side) for side in self.wrong))
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
                    self.todo.append([int(value)
                        for value in line.split('\t')])
        except IOError:
            pass

    def optimal(self, epsilon=10**-5, max_dice=50):
        """Determine optimal play using markov process
        """
        def pwin(probabilities, i, j):
            """Compute probability to win for a given situation
            """
            if i >= self.goal:
                return 1.0
            elif j >= self.goal:
                return 0.0
            else:
                return probabilities[i][j]

        dice_probs = dices.dice_probability(self.dice, max_dice, self.wrong)

        def action_probs(indexes, probabilities):
            """Compute the probability of winning for the different
            possibles actions
            """
            probs = list()
            i, j = indexes
            for k in range(1, max_dice + 1):
                total_prob = self.dice - len(self.wrong)
                total_prob = 1 - (total_prob / self.dice) ** k
                roll = total_prob * (1 - pwin(probabilities, j, i))
                for result, prob in dice_probs[k]:
                    roll += prob * (1 - pwin(probabilities, j, i + result))
                probs.append((k, roll))

            return probs

        result = markov.value_iteration([
            lambda : self.goal,
            lambda i : self.goal,
            ], epsilon, action_probs, True)

        return result


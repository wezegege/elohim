#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import math
import sys
import os.path

from elohim.bot.pig import RandomBot
from elohim.bot.utils import value_iteration, dice_probability


class HogBot(RandomBot):
    def __init__(self, dice=6, goal=100, wrong=None):
        self.dice = dice
        self.goal = goal
        self.wrong = [1] if wrong is None else wrong
        self.filename = 'hog_d{dice}w{wrong}g{goal}.txt'
        self.filename = self.filename.format(dice=dice, goal=goal,
                wrong='-'.join(str(value) for value in self.wrong))
        self.filename = os.path.join(
                os.path.dirname(__file__),
                'data',
                self.filename)
        self.todo = list()
        try:
            with open(self.filename, 'r') as content:
                for line in content:
                    self.todo.append([int(value) for value in line.split('\t')])
        except FileNotFoundError as ex:
            pass


    def optimal(self, epsilon=10**-5, max_dice=50):
        def pwin(p, i, j):
            if i >= self.goal:
                return 1.0
            elif j >= self.goal:
                return 0.0
            else:
                return p[i][j]

        dice_probs = dice_probability(self.dice, max_dice, self.wrong)

        def action_probs(indexes, p):
            probs = list()
            i, j = indexes
            for k in range(1, max_dice + 1):
                total_prob = 1 - ((self.dice - len(self.wrong)) / self.dice) ** k
                roll = total_prob * (1 - pwin(p, j, i))
                for result, prob in dice_probs[k]:
                    roll += prob * (1 - pwin(p, j, i + result))
                probs.append((k, roll))

            return probs

        result = value_iteration([
            lambda : self.goal,
            lambda i : self.goal,
            ], epsilon, action_probs, True)

        return result


#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.engine.data import Data

import os.path


class RandomBot(object):
    def send(self, message, **kwargs):
        if message == 'askcurrent':
            self.askplayer(kwargs['destination'], kwargs['options'])

    def askplayer(self, destination, options):
        result = random.choice(list(options.keys()))
        Data.set(['players', 'current'] + destination, result)


class TurnTotalBot(RandomBot):
    def __init__(self, turntotal=None, wrong=1, dice=6, goal=100):
        self.turntotal = int(dice*(dice+1)/ 2 - wrong) if turntotal is None else turntotal
        self.goal = goal

    def askplayer(self, destination, options):
        actual = Data.get(['players', 'current', 'score', 'temporary'])
        score = Data.get(['players', 'current', 'score', 'permanent'])
        if actual + score > self.goal or actual >= self.turntotal:
            result = 'hold'
        else:
            result = 'roll'
        Data.set(['players', 'current'] + destination, result)


class PigBot(RandomBot):
    def __init__(self, dice=6, goal=100, wrong=1):
        self.dice=dice
        self.goal=goal
        self.wrong=wrong
        self.filename = 'd{dice}w{wrong}g{goal}.txt'.format(dice=dice, goal=goal, wrong=wrong)
        self.filename = os.path.join(
                os.path.dirname(__file__),
                self.filename)
        self.todo = list()
        with open(self.filename, 'r') as content:
            for line in content:
                self.todo.append([int(value) for value in line.split('\t')])

    def askplayer(self, destination, options):
        current = Data.get(['players', 'current'])
        players = Data.get(['players', 'list'])

        score = current['score']['permanent']
        try:
            against = max(player['score']['permanent'] for player in players if player != current)
        except ValueError:
            against = 0
        threshold = self.todo[score][against]

        turn = current['score']['temporary']
        result = 'roll' if threshold > turn else 'hold'
        Data.set(['players', 'current'] + destination, result)

    def optimal(self, epsilon=10**-9):
        p = [[[0.0] * self.goal for a in range(self.goal)] for b in range(self.goal)]
        do_roll = [[[False] * self.goal for a in range(self.goal)] for b in range(self.goal)]

        def pwin(i, j, k):
            if i + k >= self.goal:
                return 1.0
            elif j >= self.goal:
                return 0.0
            else:
                return p[i][j][k]

        iterations = 0
        max_change = 1.0
        diffs = self.goal ** 3
        while max_change > epsilon:
            old_roll = copy.deepcopy(do_roll)
            iterations += 1
            max_change = 0.0
            for i in range(self.goal):
                for j in range(self.goal):
                    for k in range(self.goal - i):
                        old_prob = p[i][j][k]
                        roll = 0.0
                        for value in range(1, self.dice + 1):
                            if value == self.wrong:
                                roll += (1.0 - pwin(j, i, 0))
                            else:
                                roll += pwin(i, j, k + value)
                        roll /= self.dice
                        hold = 1 - pwin(j, i + k, 0)
                        p[i][j][k] = max(roll, hold)
                        do_roll[i][j][k] = (roll > hold)
                        change = math.fabs(p[i][j][k] - old_prob)
                        max_change = max(max_change, change)
            diffs = sum(1 for a in range(self.goal) for b in range(self.goal) for c in range(self.goal - a) if do_roll[a][b][c] != old_roll[a][b][c])

        result = list()

        for i in range(self.goal):
            result.append(list())
            for j in range(self.goal):
                try:
                    todo = min(k for k in range(self.goal) if not do_roll[i][j][k])
                    result[i].append(todo)
                except ValueError:
                    result[i].append(self.goal)

        with open(self.filename, 'w') as save:
            save.write('\n'.join('\t'.join(str(value) for value in line) for line in result))


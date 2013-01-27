#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.engine.data import Data

import random


class RollDiceCurrent(object):
    def __init__(self, destination, size=6):
        self.destination = destination
        self.size = size

    def player_data(self):
        return [(self.destination, 0)]

    def play(self):
        roll = random.randint(1, self.size)
        Data.get(['players', 'current', 'client']).send('roll', roll=roll)
        Data.set(['players', 'current'] + self.destination, roll)


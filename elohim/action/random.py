#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.action import Action

import random


class RollDiceCurrent(Action):
    library = 'random'
    name = 'roll-dice-current'
    parameters = [
            ('destination', 'player_data'),
            ('size', 'integer'),
            ]

    def play(self):
        roll = random.randint(1, self.values['size'])
        self.data.get(['players', 'current', 'client']).send('roll', roll=roll)
        self.data.set(['players', 'current'] + self.values['destination'], roll)


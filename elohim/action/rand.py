#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.action import Action
from elohim.action.parameter import PlayerData, ExpressionParameter

import random


class RollDiceCurrent(Action):
    library = 'random'
    name = 'roll-dice-current'
    parameters = [
            ('destination', PlayerData()),
            ('size', ExpressionParameter()),
            ]

    def play(self):
        roll = random.randint(1, self.values['size'].value())
        self.send('roll', roll=roll)
        destination = ['players', 'current'] + self.values['destination']
        self.data.set(destination, roll)


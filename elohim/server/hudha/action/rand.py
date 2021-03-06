#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Random related actions
"""

from elohim.action import Action
from elohim.action.parameter import PlayerData, ExpressionParameter

import random


namespace = action.action.namespace('__name__')


@namespace.entity('roll-dice-current')
class RollDiceCurrent(Action):
    """Roll dice with given size for current player
    """
    parameters = [
            ('destination', PlayerData()),
            ('size', ExpressionParameter()),
            ]

    def play(self):
        roll = random.randint(1, self.values['size'].value())
        self.send('roll', roll=roll)
        destination = ['players', 'current'] + self.values['destination']
        self.data.set(destination, roll)


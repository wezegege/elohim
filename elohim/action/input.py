#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Library for handling interactions with player
"""

from elohim.action import Action
from elohim.action.parameter import PlayerData, ValueParameter


class AskPlayer(Action):
    """Meet current player with choices
    """
    library = 'input'
    name = 'ask-player'
    parameters = [
            ('destination', PlayerData()),
            ('options', ValueParameter()),
            ]

    def play(self):
        result = self.askcurrent(self.values['options'])
        destination = ['players', 'current'] + self.values['destination']
        self.send('choice', choice=result)
        self.data.set(destination, result)

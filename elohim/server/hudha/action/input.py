#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Library for handling interactions with player
"""

from elohim import action
from elohim.action import parameter


namespace = action.action.namespace(__name__)


@namespace.entity('ask-player')
class AskPlayer(action.Action):
    """Meet current player with choices
    """
    parameters = [
            ('destination', parameter.PlayerData()),
            ('options', parameter.ValueParameter()),
            ]

    def play(self):
        result = self.askcurrent(self.values['options'])
        destination = ['players', 'current'] + self.values['destination']
        self.send('choice', choice=result)
        self.data.set(destination, result)

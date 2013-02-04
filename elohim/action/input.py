#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.action import Action
from elohim.action.parameter import PlayerData, ValueParameter


class AskPlayer(Action):
    library = 'input'
    name = 'ask-player'
    parameters = [
            ('destination', PlayerData()),
            ('options', ValueParameter()),
            ]

    def play(self):
        self.data.get(['players', 'current', 'client']).send(
                'askcurrent',
                destination=self.values['destination'],
                options=self.values['options'])

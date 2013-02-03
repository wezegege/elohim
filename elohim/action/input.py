#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.action import Action


class AskPlayer(Action):
    library = 'input'
    name = 'ask-player'
    parameters = [
            ('destination', 'player_data'),
            ('options', 'value'),
            ]

    def play(self):
        self.data.get(['players', 'current', 'client']).send(
                'askcurrent',
                destination=self.values['destination'],
                options=self.values['options'])

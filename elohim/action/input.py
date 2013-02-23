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
        result = self.send('askcurrent', options=self.values['options'])
        destination = ['players', 'current'] + self.values['destination']
        self.send('choice', choice=result)
        self.data.set(destination, result)

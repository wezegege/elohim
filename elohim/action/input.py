#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.engine.data import Data


class AskPlayer(object):
    def __init__(self, destination, options):
        self.destination = destination
        self.options = options

    def player_data(self):
        return [(self.destination, '')]

    def play(self):
        Data.get(['players', 'current', 'client']).send('askcurrent', destination=self.destination, options=self.options)

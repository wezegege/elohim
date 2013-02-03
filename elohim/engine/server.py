#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.engine.data import Data

class Server(object):
    def __init__(self, rules):
        self.rules = rules
        self.data = Data(rules.player_data())
        self.rules.set_data(self.data)

    def add_player(self, name, client):
        self.data.add_player(name, client)

    def play(self):
        self.rules.play()


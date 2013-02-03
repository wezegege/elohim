#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.engine.data import Data
from elohim.action import Entity

class Server(object):
    def __init__(self, rules, defaults):
        self.rules = rules
        Data.init(rules.player_data(), defaults)
        #self.data = Data(rules.player_data())
        self.data = Data
        self.rules.set_data(self.data)

    def add_player(self, name, client):
        self.data.add_player(name, client)

    def play(self):
        self.rules.play()

    def to_dict(self):
        metadata = {
                'defaults' : self.data.defaults,
                'rules' : self.rules.to_dict(),
                }
        return metadata

    @classmethod
    def from_dict(cls, gamedata):
        rules = Entity.from_dict(gamedata['rules'])
        return cls(rules=rules, defaults=gamedata['defaults'])


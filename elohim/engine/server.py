#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.engine.data import Data
from elohim.action import Entity

import json

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

    def to_json(self):
        metadata = {
                'defaults' : self.data.defaults,
                'rules' : self.rules.to_dict(),
                }
        print(json.dumps(metadata, sort_keys=True, indent=4))

    @classmethod
    def from_json(cls, filename):
        with open(filename, 'r') as content:
            gamedata = json.load(content)
        rules = Entity.from_dict(gamedata['rules'])
        return cls(rules=rules, defaults=gamedata['defaults'])


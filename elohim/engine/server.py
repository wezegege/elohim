#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.engine import data
from elohim import action

class Server(object):
    def __init__(self, rules, defaults, settings):
        self.rules = rules
        data.Data.init(rules.player_data(), defaults, settings)
        #self.data = data.Data(rules.player_data())
        self.data = data.Data
        self.rules.set_data(self.data)

    def add_player(self, name, client):
        self.data.add_player(name, client)

    def play(self):
        self.rules.play()

    def to_dict(self):
        defaults = {'::'.join(field) : value for field, value in self.data.defaults}
        settings = {'::'.join(field) : value for field, value in self.data.settings}
        metadata = {
                'defaults' : defaults,
                'rules' : self.rules.to_dict(),
                }
        return metadata

    @classmethod
    def from_dict(cls, gamedata):
        rules = action.Entity.from_dict(gamedata['rules'])
        defaults = [(field.split('::'), value) for field, value in gamedata['defaults'].items()]
        settings = [(entry['name'].split('::'), entry['default']) for entry in gamedata['settings']]
        return cls(rules=rules, defaults=defaults, settings=settings)


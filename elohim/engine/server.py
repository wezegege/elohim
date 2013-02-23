#!/usr/bin/env python
# -*- coding: utf-8 -*-
from elohim.engine import data
from elohim import action

class Server(object):
    def __init__(self, **kwargs):
        self.rules = kwargs['rules']
        #data.Data.init(self.rules.player_data(), kwargs.get('defaults', dict()))
        #self.data = data.Data
        self.data = data.Data(player_data=self.rules.player_data(),
                variables=kwargs.get('variables', dict()))
        for field, value in kwargs.get('settings', list()):
            self.data.set(field, value)
        for field, value in kwargs.get('metadata', dict()).items():
            self.data.set(field, value)
        self.rules.set_data(self.data)

    def add_player(self, name, client):
        self.data.add_player(name, client)
        client.set_data(self.data)

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
        variables = [(field.split('::'), value) for field, value in gamedata['variables'].items()]
        settings = [(entry['name'].split('::'), entry['default']) for entry in gamedata['settings']]
        return cls(rules=rules, variables=variables, settings=settings)


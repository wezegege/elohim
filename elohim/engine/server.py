#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.engine import data
from elohim import action

class Server(object):
    def __init__(self, **kwargs):
        self.rules = kwargs['rules']
        #data.Data.init(self.rules.player_data(), kwargs.get('defaults', dict()))
        #self.data = data.Data
        #self.data = data.Data(player_data=self.rules.player_data(),
        #        variables=kwargs.get('variables', dict()))
        self.player_data = self.rules.player_data()
        self.variables = kwargs.get('variables', dict())
        self.data = data.Entry()
        for dataset in [
                (
                    (['players', 'count'], 0),
                    (['players', 'index'], 0),
                ),
                kwargs.get('settings', list()),
                kwargs.get('metadata', dict()).items(),
                ]:
            for field, value in dataset:
                self.data.set(field, value)
        def current_reference(root):
            index = root.get(['players', 'index'])
            players = root.get(['players', 'list'])
            if index in players:
                return players.get([index])
            else:
                raise IndexError
        self.data.refer(['players', 'current'], current_reference)

        self.rules.set_data(self.data)

    def add_player(self, name, client):
        index = self.data.get(['players', 'count'])
        self.data.add(['players', 'count'], 1)
        for field in self.player_data:
            for indexed, parameters in self.variables:
                if field == indexed:
                    self.data.set(['players', 'list', index] + field, parameters.get('default', None))
                    break
            else:
                self.data.set(['players', 'list', index] + field, None)
        for field, value in (
                ('name', name),
                ('client', client),
                ('ingame', True),
                ):
            self.data.set(['players', 'list', index, field], value)

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


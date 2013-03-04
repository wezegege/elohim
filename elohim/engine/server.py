#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.engine import data
from elohim import action

class Server(object):
    def __init__(self, **kwargs):
        self.rules = kwargs['rules']
        self.player_data = self.rules.player_data()
        self.variables = kwargs.get('variables', dict())
        self.data = data.Entry()
        for dataset in [
                (
                    (['players', 'count'], 0),
                    (['players', 'index'], -1),
                ),
                kwargs.get('settings', list()),
                kwargs.get('metadata', dict()).items(),
                ]:
            for field, value in dataset:
                self.data.set(field, value)

        self.data.refer(['players', 'current'],
                'players::list::<players::index>')

        self.rules.set_data(self.data)

    def add_player(self, name, client):
        index = self.data.get(['players', 'count'])
        self.data.add(['players', 'count'], 1)
        for field, config in self.variables:
            self.data.getdefault(
                    ['players', 'list', index]).configure(field, **config)
        for field, value in (
                ('name', name),
                ('client', client),
                ('ingame', True),
                ):
            self.data.set(['players', 'list', index, field], value)

        client.set_data(self.data)

    def play(self):
        self.data.initialize()
        self.rules.play()

    def to_dict(self):
        metadata = {
                'rules' : self.rules.to_dict(),
                }
        return metadata

    @classmethod
    def from_dict(cls, gamedata):
        rules = action.Entity.from_dict(gamedata['rules'])
        variables = [(field.split('::'), value)
                for field, value in gamedata['variables'].items()]
        settings = [(entry['name'].split('::'), entry['default'])
                for entry in gamedata['settings']]
        return cls(rules=rules, variables=variables, settings=settings)


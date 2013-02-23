#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Data(object):

    def __init__(self, player_data=None, variables=None):
        self.content = dict()
        self.set(['players', 'list'], list())
        self.set(['players', 'count'], 0)
        self.set(['players', 'index'], -1)
        self.player_data = list() if player_data is None else player_data
        self.variables = dict() if variables is None else variables

    def add_player(self, name, client):
        index = self.get(['players', 'count'])
        self.add(['players', 'count'], 1)
        for field in self.player_data:
            for indexed, parameters in self.variables:
                if field == indexed:
                    self.set(['players', 'list', index] + field, parameters.get('default', None))
                    break
            else:
                self.set(['players', 'list', index] + field, None)
        for field, value in (
                ('name', name),
                ('client', client),
                ('ingame', True),
                ):
            self.set(['players', 'list', index, field], value)

    def get(self, index, element=None):
        result = self.content if element is None else element
        for entry in index:
            result = result[entry]
        return result

    def set(self, index, value):
        result = self.content
        for entry in index[:-1]:
            if isinstance(result, dict) and entry not in result:
                result[entry] = dict()
            elif isinstance(result, list) and len(result) >= entry:
                for count in range(entry + 1 - len(result)):
                    result.append(dict())
            result = result[entry]
        result[index[-1]] = value
        return value

    def add(self, index, value):
        entry = self.get(index)
        self.set(index, entry + value)


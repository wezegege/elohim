#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Data(object):
    content = dict()

    @classmethod
    def init(cls, variables=None):
        cls.set(['players', 'list'], list())
        cls.set(['players', 'count'], 0)
        cls.set(['players', 'index'], -1)
        cls.player_data = list() if variables is None else variables

    @classmethod
    def add_player(cls, name, client):
        index = cls.get(['players', 'count'])
        cls.add(['players', 'count'], 1)
        for field, default in [(['name'], name), (['client'], client),
                (['ingame'], True)] + cls.player_data:
            cls.set(['players', 'list', index] + field, default)

    @classmethod
    def get(cls, index, element=None):
        result = cls.content if element is None else element
        for entry in index:
            result = result[entry]
        return result

    @classmethod
    def set(cls, index, value):
        result = cls.content
        for entry in index[:-1]:
            if isinstance(result, dict) and entry not in result:
                result[entry] = dict()
            elif isinstance(result, list) and len(result) >= entry:
                for count in range(entry + 1 - len(result)):
                    result.append(dict())
            result = result[entry]
        result[index[-1]] = value
        return value

    @classmethod
    def add(cls, index, value):
        entry = cls.get(index)
        cls.set(index, entry + value)


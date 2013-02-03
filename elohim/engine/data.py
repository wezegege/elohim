#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Data(object):
    content = dict()
    defaults = dict()

    @classmethod
    def init(cls, variables=None, defaults=None, settings=None):
        cls.set(['players', 'list'], list())
        cls.set(['players', 'count'], 0)
        cls.set(['players', 'index'], -1)
        cls.player_data = list() if variables is None else variables
        cls.defaults = list() if defaults is None else defaults
        cls.settings = list() if settings is None else settings
        for field, value in cls.settings:
            cls.set(field, value)

    @classmethod
    def add_player(cls, name, client):
        index = cls.get(['players', 'count'])
        cls.add(['players', 'count'], 1)
        for field in cls.player_data:
            for indexed, default in cls.defaults:
                if field  == indexed:
                    cls.set(['players', 'list', index] + field, default)
                    break
            else:
                cls.set(['players', 'list', index] + field, None)
        cls.set(['players', 'list', index, 'name'], name)
        cls.set(['players', 'list', index, 'client'], client)
        cls.set(['players', 'list', index, 'ingame'], True)

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


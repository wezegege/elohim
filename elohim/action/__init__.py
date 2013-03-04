#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.utils import classes
import collections


class NonExistingEntity(Exception):
    def __init__(self, library, name):
        message = 'Entity not found : {name} in library {library}'.format(
                name=name, library=library)
        super(NonExistingEntity, self).__init__(message)


class Entity(object):
    type = 'entity'
    parameters = list()
    name = 'entity'
    library = 'core'

    def __init__(self, **kwargs):
        if not hasattr(self, 'values'):
            self.values = dict()
        for field, field_type, in self.parameters:
            if field in kwargs:
                self.values[field] = kwargs[field]
                del kwargs[field]
            else:
                self.values[field] = field_type.default()
        super(Entity, self).__init__(**kwargs)
        self.data = None

        self.init()

    def init(self):
        pass

    def player_data(self):
        result = list()
        for field, field_type, in self.parameters:
            result.extend(field_type.player_data(self.values[field]))
        return result

    def set_data(self, data):
        self.data = data
        for field, field_type, in self.parameters:
            field_type.set_data(self.values[field], data)

    def to_dict(self):
        result = {
                'name' : self.name,
                'library' : self.library,
                }
        for field, field_type in self.parameters:
            result[field] = field_type.to_dict(self.values[field])
        return result

    @classmethod
    def from_dict(cls, rules):
        if not hasattr(cls, 'entities'):
            cls.entities = cls.list_entities()
        entity = cls.entities.get(
                rules['library'], dict()).get(rules['name'], None)
        if entity is None:
            raise NonExistingEntity(rules['library'], rules['name'])
        del rules['library']
        del rules['name']
        for field, field_type in entity.parameters:
            rules[field] = field_type.from_dict(rules[field])
        return entity(**rules)

    @classmethod
    def list_entities(cls):
        subs = classes.list_subclasses(cls, __name__, __path__)
        result = collections.defaultdict(dict)
        for sub in subs:
            result[sub.library][sub.name] = sub
        return result

class Action(Entity):
    library = 'action'
    name = 'action'
    type = 'action'

    def play(self):
        pass

    def send(self, message, **kwargs):
        for player in self.data.get(['players', 'list']):
            player.get(['client']).send(message, **kwargs)

    def askcurrent(self, options):
        current = self.data.get(['players', 'current', 'client'])
        return current.askplayer(options)

class Expression(Entity):
    library = 'expression'
    name = 'expression'
    type = 'expression'

    def value(self, **_kwargs):
        return None


class Condition(Entity):
    library = 'condition'
    name = 'condition'
    type = 'condition'

    def evaluate(self, **_kwargs):
        return True


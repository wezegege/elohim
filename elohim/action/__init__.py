#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pkgutil


class NonExistingEntity(Exception):
    def __init__(self, library, name):
        message = 'Entity not found : {name} in library {library}'.format(name=name, library=library)
        super(NonExistingEntity, self).__init__(message)


class Entity(object):
    type = 'entity'
    parameters = list()
    name = 'entity'
    library = 'core'

    def __init__(self, **kwargs):
        self.values = dict()
        for field, field_type, *args in self.parameters:
            if field in kwargs:
                self.values[field] = kwargs[field]
            else:
                self.values[field] = field_type.default()

    def player_data(self):
        result = list()
        for field, field_type, *args in self.parameters:
            result.extend(field_type.player_data(self.values[field]))
        return result

    def set_data(self, data):
        self.data = data
        for field, field_type, *args in self.parameters:
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
        entity = cls.entities.get(rules['library'], dict()).get(rules['name'], None)
        if entity is None:
            raise NonExistingEntity(rules['library'], rules['name'])
        del rules['library']
        del rules['name']
        for field, field_type in entity.parameters:
            rules[field] = field_type.from_dict(rules[field])
        return entity(**rules)

    @classmethod
    def find_subclasses(cls, seen):
        try:
            subs = cls.__class__.__subclasses__()
        except TypeError:
            subs = cls.__class__.__subclasses__(cls)
        for sub in subs:
            if not sub.library in seen:
                seen[sub.library] = dict()
            if not sub.name in seen[sub.library]:
                seen[sub.library][sub.name] = sub
                sub.find_subclasses(seen)

    @classmethod
    def list_entities(self):
        for _f, submodule, _i in pkgutil.walk_packages(__path__, __name__ + '.'):
            __import__(submodule)
        result = dict()
        self.find_subclasses(result)
        return result


class Action(Entity):
    library='action'
    name='action'
    type='action'

    def play(self):
        pass

class Expression(Entity):
    library='expression'
    name='expression'
    type='expression'

    def value(self, **kwargs):
        return None


class Condition(Entity):
    library='condition'
    name='condition'
    type='condition'

    def evaluate(self, **kwargs):
        return True


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pkgutil


class NonExistingEntity(Exception):
    def __init__(self, library, name):
        message = 'Entity not found : {name} in library {library}'.format(name=name, library=library)
        super(NonExistingEntity, self).__init__(message)


def default(field_type, args=None):
    answers = {
            'expression_list' : lambda : list(),
            'expression' : lambda : Expression(),
            'player_data' : lambda : list(),
            'condition_list' : lambda : list(),
            'condition' : lambda : Condition(),
            'actions' : lambda : list(),
            'value' : None,
            'integer' : 0,
            }
    if args:
        result = args[0]
    elif field_type in answers:
        result = answers[field_type]
    else:
        result = None
    if hasattr(result, '__call__'):
        result = result()
    return result


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
                self.values[field] = default(field_type, args)

    def player_data(self):
        result = list()
        for field, field_type, *args in self.parameters:
            if field_type in ('player_data',):
                result.append(self.values[field])
            elif field_type in ('expression', 'condition'):
                result.extend(self.values[field].player_data())
            elif field_type in ('expression_list', 'condition_list', 'actions'):
                for entity in self.values[field]:
                    result.extend(entity.player_data())
        return result

    def set_data(self, data):
        self.data = data
        for field, field_type, *args in self.parameters:
            if field_type in ('expression', 'condition'):
                self.values[field].set_data(data)
            elif field_type in ('expression_list', 'condition_list', 'actions'):
                for entity in self.values[field]:
                    entity.set_data(data)

    def to_dict(self):
        result = {
                'name' : self.name,
                'library' : self.library,
                }
        for field, field_type in self.parameters:
            if field_type in ('actions', 'condition_list', 'expression_list'):
                result[field] = [value.to_dict() for value in self.values[field]]
            elif field_type in ('condition', 'expression'):
                result[field] = self.values[field].to_dict()
            else:
                result[field] = self.values[field]
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
            if field_type in ('actions', 'condition_list', 'expression_list'):
                rules[field] = [cls.from_dict(entity) for entity in rules[field]]
            elif field_type in ('condition', 'expression'):
                rules[field] = cls.from_dict(rules[field])
        return entity(**rules)


    def represent(self, indent=1):
        indent_size = 2
        result = "{library}/{name} ({type}) {{\n".format(
                name=self.name,
                library=self.library,
                type=self.type)
        for field, field_type in self.parameters:
            result += "{indent}{field} ({field_type}) : ".format(
                    indent=' ' * (indent * indent_size),
                    field=field,
                    field_type=field_type)
            if field_type in ('actions', 'condition_list', 'expression_list'):
                result += '[\n'
                for value in self.values[field]:
                    result += '{indent}{description}'.format(
                            indent=' ' * ((indent + 1) * indent_size),
                            description=value.represent(indent=indent + 2))
                result += '{indent}]\n'.format(
                        indent=' ' * ((indent) * indent_size)
                        )
            elif field_type in ('condition', 'expression'):
                result += self.values[field].represent(indent=indent + 1)
            else:
                result += '{value}\n'.format(value=self.values[field])
        result += '{indent}}}\n'.format(indent=' ' * ((indent - 1) * indent_size))
        return result

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


class Expression(Entity):
    library='core'
    name='expression'
    type='expression'

    def value(self, **kwargs):
        return None


class Condition(Entity):
    library='core'
    name='condition'
    type='condition'

    def evaluate(self, **kwargs):
        return True


class Action(Entity):
    library='core'
    name='action'
    type='action'

    def play(self):
        pass

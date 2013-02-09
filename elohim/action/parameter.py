#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.action import Expression, Condition, Entity


class Unset(object):
    pass


class Parameter(Entity):
    library = 'parameter'
    name = 'parameter'
    type = 'parameter'

    def __init__(self, default=Unset, mandatory=True):
        self.default_value = default
        self.mandatory=mandatory

    def default(self):
        return None if self.default_value is Unset else self.default_value

    def player_data(self, value):
        return list()

    def set_data(self, _value, _data):
        pass

    def to_dict(self, value):
        return value

    def from_dict(self, value):
        return value


class EntityParameter(Parameter):
    library = 'parameter'
    name = 'entity-parameter'

    def player_data(self, value):
        return value.player_data()

    def set_data(self, value, data):
        value.set_data(data)

    def to_dict(self, value):
        return value.to_dict()

    def from_dict(self, value):
        return Entity.from_dict(value)


class EntityList(Parameter):
    library = 'parameter'
    name = 'entity-list'

    def default(self):
        return list() if self.default is Unset else self.default

    def player_data(self, value):
        result = list()
        for entity in value:
            result.extend(entity.player_data())
        return result

    def set_data(self, value, data):
        for entity in value:
            entity.set_data(data)

    def to_dict(self, value):
        return [entity.to_dict() for entity in value]

    def from_dict(self, value):
        return [Entity.from_dict(entity) for entity in value]


class ExpressionList(EntityList):
    library = 'parameter'
    name = 'expression-list'


class ExpressionParameter(EntityParameter):
    library = 'parameter'
    name = 'expression-parameter'

    def default(self):
        return Expression() if self.default is Unset else self.default


class ConditionParameter(EntityParameter):
    library = 'parameter'
    name = 'condition-parameter'

    def default(self):
        return Condition() if self.default is Unset else self.default


class VariableParameter(Parameter):
    library = 'parameter'
    name = 'variable-parameter'

    def to_dict(self, value):
        return '::'.join(value)

    def from_dict(self, value):
        return value.split('::')


class PlayerData(VariableParameter):
    library = 'parameter'
    name = 'player-data'

    def player_data(self, value):
        return [value]

class GlobalData(VariableParameter):
    library = 'parameter'
    name = 'global-data'

class ActionList(EntityList):
    library = 'parameter'
    name = 'action-list'

class ValueParameter(Parameter):
    library = 'parameter'
    name = 'value-parameter'

class IntegerParameter(Parameter):
    library = 'parameter'
    name = 'integer'

    def __init__(self, mini=None, maxi=None, **kwargs):
        super().__init__(**kwargs)
        self.mini, self.maxi = mini, maxi

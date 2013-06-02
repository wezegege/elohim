#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Parameter for an entity
"""

from elohim.action import Expression, Condition, Entity


Unset = type('Unset', (object,), dict())


class Parameter(Entity):
    """Base class for a Parameter
    """
    library = 'parameter'
    name = 'parameter'
    type = 'parameter'

    def __init__(self, default=Unset, mandatory=True, **kwargs):
        super(Parameter, self).__init__(**kwargs)
        self.default_value = default
        self.mandatory = mandatory

    def default(self):
        """Default value for the parameter
        """
        return None if self.default_value is Unset else self.default_value

    def get_player_data(self, _value):
        """Get player variable required by entitites in order to work
        """
        return list()

    def register_data(self, _value, _data):
        """Store data to parameters whenever they need it
        """
        pass

    def value_to_dict(self, value):
        """Transform parameter to a python dictionary
        """
        return value

    def value_from_dict(self, value):
        """Convert standard value to convenience
        """
        return value


class EntityParameter(Parameter):
    """Parameter which represent an entity
    """
    library = 'parameter'
    name = 'entity-parameter'

    def get_player_data(self, value):
        return value.player_data()

    def register_data(self, value, data):
        value.set_data(data)

    def value_to_dict(self, value):
        return value.to_dict()

    def value_from_dict(self, value):
        return Entity.from_dict(value)


class EntityList(Parameter):
    """Parameter which represent a list of entities
    """
    library = 'parameter'
    name = 'entity-list'

    def default(self):
        return list() if self.default is Unset else self.default

    def get_player_data(self, value):
        result = list()
        for entity in value:
            result.extend(entity.player_data())
        return result

    def register_data(self, value, data):
        for entity in value:
            entity.set_data(data)

    def value_to_dict(self, value):
        return [entity.to_dict() for entity in value]

    def value_from_dict(self, value):
        return [Entity.from_dict(entity) for entity in value]


class ExpressionList(EntityList):
    """A parameter which represent a list of expressions
    """
    library = 'parameter'
    name = 'expression-list'


class ExpressionParameter(EntityParameter):
    """A parameter which represent an expression
    """
    library = 'parameter'
    name = 'expression-parameter'

    def default(self):
        return Expression() if self.default is Unset else self.default


class ConditionParameter(EntityParameter):
    """A parameter which represent a condition
    """
    library = 'parameter'
    name = 'condition-parameter'

    def default(self):
        return Condition() if self.default is Unset else self.default


class VariableParameter(Parameter):
    """A parameter which represent a variable
    """
    library = 'parameter'
    name = 'variable-parameter'

    def value_to_dict(self, value):
        return '::'.join(value)

    def value_from_dict(self, value):
        return value.split('::')


class PlayerData(VariableParameter):
    """A parameter which represent a player variable
    """
    library = 'parameter'
    name = 'player-data'

    def get_player_data(self, value):
        return [value]

class GlobalData(VariableParameter):
    """A parameter which represent a global variable
    """
    library = 'parameter'
    name = 'global-data'

class ActionList(EntityList):
    """A parameter which represent a list of actions
    """
    library = 'parameter'
    name = 'action-list'

class ValueParameter(Parameter):
    """A parameter which represent a constant
    """
    library = 'parameter'
    name = 'value-parameter'

class IntegerParameter(Parameter):
    """A parameter which represent an integer
    """
    library = 'parameter'
    name = 'integer'

    def __init__(self, mini=None, maxi=None, **kwargs):
        super(IntegerParameter, self).__init__(**kwargs)
        self.mini, self.maxi = mini, maxi

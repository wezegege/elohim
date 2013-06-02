#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Rule library for the turn-based rule engine system
"""

from elohim.utils import classes
import collections


class NonExistingEntity(Exception):
    """Exception raised when founding an unknown rule name
    """
    def __init__(self, library, name):
        message = 'Entity not found : {name} in library {library}'.format(
                name=name, library=library)
        super(NonExistingEntity, self).__init__(message)


class Entity(object):
    """Base class for a rule
    """
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

        if hasattr(self, 'init'):
            getattr(self, 'init')()

    def player_data(self):
        """Look for variables used by this rule, and relative to a player
        """
        result = list()
        for field, field_type, in self.parameters:
            result.extend(field_type.get_player_data(self.values[field]))
        return result

    def set_data(self, data):
        """Register the reference to the data tree root
        """
        self.data = data
        for field, field_type, in self.parameters:
            field_type.register_data(self.values[field], data)

    def to_dict(self):
        """Transform rule to a python dictionary
        """
        result = {
                'name' : self.name,
                'library' : self.library,
                }
        for field, field_type in self.parameters:
            result[field] = field_type.value_to_dict(self.values[field])
        return result

    @classmethod
    def from_dict(cls, rules):
        """Create the rule given a python dictionary
        """
        if not hasattr(cls, 'entities'):
            cls.entities = cls.list_entities()
        entity = cls.entities.get(
                rules['library'], dict()).get(rules['name'], None)
        if entity is None:
            raise NonExistingEntity(rules['library'], rules['name'])
        del rules['library']
        del rules['name']
        for field, field_type in entity.parameters:
            rules[field] = field_type.value_from_dict(rules[field])
        return entity(**rules)

    @classmethod
    def list_entities(cls):
        """Search for all instance of Entity, which correspond to all
        existing rules installed
        """
        subs = classes.list_subclasses(cls, __name__, __path__)
        result = collections.defaultdict(dict)
        for sub in subs:
            result[sub.library][sub.name] = sub
        return result

class Action(Entity):
    """Base class for an action rule, which using affects the game state
    """
    library = 'action'
    name = 'action'
    type = 'action'

    def play(self):
        """Main function for an action which describe the effects to be
        applied to the game state
        """
        pass

    def send(self, message, **kwargs):
        """Helper method to send a message to the player
        """
        for player in self.data.get(['players', 'list']):
            player.get(['client']).send(message, **kwargs)

    def askcurrent(self, options):
        """Ask the current player for a choice
        """
        current = self.data.get(['players', 'current', 'client'])
        return current.askplayer(options)

class Expression(Entity):
    """Base class for an expression, which correspond to a mathematical
    expression
    """
    library = 'expression'
    name = 'expression'
    type = 'expression'

    def value(self, **_kwargs):
        """Determine the value of the expression
        """
        return None


class Condition(Entity):
    """Base class for a condition
    """
    library = 'condition'
    name = 'condition'
    type = 'condition'

    def evaluate(self, **_kwargs):
        """Determine whether the content of the condition can be evaluated
        as true or false
        """
        return True


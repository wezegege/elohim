#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Rule library for conditions
"""


from elohim import action
from elohim.action import parameter


class Equals(action.Condition):
    """Equality condition
    """
    library = 'condition'
    name = 'equals'
    parameters = [
            ('expressions', parameter.ExpressionList()),
            ]

    def evaluate(self, **kwargs):
        expressions = self.values['expressions']
        return not expressions or \
                all(expressions[0].value(**kwargs) ==
                        expression.value(**kwargs)
                        for expression in expressions[1:])


class GreaterEquals(action.Condition):
    """Greater of equals condition
    """
    library = 'condition'
    name = 'greater-equals'
    parameters = [
            ('left', parameter.ExpressionParameter()),
            ('right', parameter.ExpressionParameter()),
            ]

    def evaluate(self, **kwargs):
        left = self.values['left'].value(**kwargs)
        right = self.values['right'].value(**kwargs)
        return bool(left >= right)


class Greater(action.Condition):
    """Greater condition
    """
    library = 'condition'
    name = 'greater'
    parameters = [
            ('left', parameter.ExpressionParameter()),
            ('right', parameter.ExpressionParameter()),
            ]

    def evaluate(self, **kwargs):
        left = self.values['left'].value(**kwargs)
        right = self.values['right'].value(**kwargs)
        return bool(left > right)


class In(action.Condition):
    """Condition which, given an item and a sequence, determines if the item
    is contained by the container
    """
    library = 'condition'
    name = 'in'
    parameters = [
            ('element', parameter.ExpressionParameter()),
            ('list', parameter.ExpressionParameter()),
            ]

    def evaluate(self, **kwargs):
        element = self.values['element'].value(**kwargs)
        container = self.values['list'].value()
        return element in container

class All(action.Condition):
    """Condition which is evaluated for all players
    """
    library = 'condition'
    name = 'all'
    parameters = [
            ('condition', parameter.ConditionParameter()),
            ]

    def evaluate(self):
        condition = self.values['condition']
        return all(condition.evaluate(player=player)
                for player in self.data.get(['players', 'list']))

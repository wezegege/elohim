#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Rule library for conditions
"""


from elohim import action
from elohim.action import parameter


namespace = action.condition.namespace(__name__)


@namespace.entity('equals')
class Equals(action.Condition):
    """Equality condition
    """
    parameters = [
            ('expressions', parameter.ExpressionList()),
            ]

    def evaluate(self, **kwargs):
        expressions = self.values['expressions']
        return not expressions or \
                all(expressions[0].value(**kwargs) ==
                        expression.value(**kwargs)
                        for expression in expressions[1:])


@namespace.entity('greater-equals')
class GreaterEquals(action.Condition):
    """Greater of equals condition
    """
    parameters = [
            ('left', parameter.ExpressionParameter()),
            ('right', parameter.ExpressionParameter()),
            ]

    def evaluate(self, **kwargs):
        left = self.values['left'].value(**kwargs)
        right = self.values['right'].value(**kwargs)
        return bool(left >= right)


@namespace.entity('greater')
class Greater(action.Condition):
    """Greater condition
    """
    parameters = [
            ('left', parameter.ExpressionParameter()),
            ('right', parameter.ExpressionParameter()),
            ]

    def evaluate(self, **kwargs):
        left = self.values['left'].value(**kwargs)
        right = self.values['right'].value(**kwargs)
        return bool(left > right)


@namespace.entity('in')
class In(action.Condition):
    """Condition which, given an item and a sequence, determines if the item
    is contained by the container
    """
    parameters = [
            ('element', parameter.ExpressionParameter()),
            ('list', parameter.ExpressionParameter()),
            ]

    def evaluate(self, **kwargs):
        element = self.values['element'].value(**kwargs)
        container = self.values['list'].value()
        return element in container


@namespace.entity('all')
class All(action.Condition):
    """Condition which is evaluated for all players
    """
    parameters = [
            ('condition', parameter.ConditionParameter()),
            ]

    def evaluate(self):
        condition = self.values['condition']
        return all(condition.evaluate(player=player)
                for player in self.data.get(['players', 'list']))

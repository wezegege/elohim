#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim import action
from elohim.action import parameter


class Equals(action.Condition):
    library = 'condition'
    name = 'equals'
    parameters = [
            ('expressions', parameter.ExpressionList()),
            ]

    def evaluate(self, **kwargs):
        expressions = self.values['expressions']
        return not expressions or \
                all(expressions[0].value(**kwargs) == expression.value(**kwargs)
                        for expression in expressions[1:])


class GreaterEquals(action.Condition):
    library = 'condition'
    name = 'greater-equals'
    parameters = [
            ('left', parameter.ExpressionParameter()),
            ('right', parameter.ExpressionParameter()),
            ]

    def evaluate(self, **kwargs):
        return bool(self.values['left'].value(**kwargs) >= self.values['right'].value(**kwargs))


class Greater(action.Condition):
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
    library = 'condition'
    name = 'in'
    parameters = [
            ('element', parameter.ExpressionParameter()),
            ('list', parameter.ExpressionParameter()),
            ]

    def evaluate(self, **kwargs):
        return self.values['element'].value(**kwargs) in self.values['list'].value()

class All(action.Condition):
    library = 'condition'
    name = 'all'
    parameters = [
            ('condition', parameter.ConditionParameter()),
            ]

    def evaluate(self):
        condition = self.values['condition']
        return all(condition.evaluate(player=player)
                for player in self.data.get(['players', 'list']))

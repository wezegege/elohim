#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.action import Condition
from elohim.action.parameter import ExpressionList, ExpressionParameter, ConditionParameter


class Equals(Condition):
    library = 'condition'
    name = 'equals'
    parameters = [
            ('expressions', ExpressionList()),
            ]

    def evaluate(self, **kwargs):
        expressions = self.values['expressions']
        return not expressions or \
                all(expressions[0].value(**kwargs) == expression.value(**kwargs)
                        for expression in expressions[1:])


class GreaterEquals(Condition):
    library = 'condition'
    name = 'greater-equals'
    parameters = [
            ('left', ExpressionParameter()),
            ('right', ExpressionParameter()),
            ]

    def evaluate(self, **kwargs):
        return self.values['left'].value(**kwargs) >= \
                self.values['right'].value(**kwargs)


class Greater(Condition):
    library = 'condition'
    name = 'greater'
    parameters = [
            ('left', ExpressionParameter()),
            ('right', ExpressionParameter()),
            ]

    def evaluate(self, **kwargs):
        return self.values['left'].value(**kwargs) > \
                self.values['right'].value(**kwargs)


class In(Condition):
    library = 'condition'
    name = 'in'
    parameters = [
            ('element', ExpressionParameter()),
            ('list', ExpressionParameter()),
            ]

    def evaluate(self, **kwargs):
        return self.values['element'].value(**kwargs) in self.values['list'].value()

class All(Condition):
    library = 'condition'
    name = 'all'
    parameters = [
            ('condition', ConditionParameter()),
            ]

    def evaluate(self):
        condition = self.values['condition']
        return all(condition.evaluate(player=player)
                for player in self.data.get(['players', 'list']))

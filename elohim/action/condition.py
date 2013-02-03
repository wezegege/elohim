#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.action import Condition, Expression


class Value(Expression):
    library = 'core'
    name = 'value'
    parameters = [
            ('value', 'value'),
            ]

    def value(self, **kwargs):
        return self.values['value']


class PlayerVariable(Expression):
    library = 'core'
    name = 'variable'
    parameters = [
            ('variable', 'player_data'),
            ]

    def value(self, **kwargs):
        if 'player' in kwargs:
            return self.data.get(self.values['variable'], kwargs['player'])
        else:
            return self.data.get(['players', 'current'] +
                    self.values['variable'])


class Sum(Expression):
    library = 'core'
    name = 'sum'
    parameters = [
            ('expressions', 'expression_list'),
            ]

    def value(self, **kwargs):
        return sum(expression.value(**kwargs)
                for expression in self.values['expressions'])


class Equals(Condition):
    library = 'core'
    name = 'equals'
    parameters = [
            ('expressions', 'expression_list'),
            ]

    def evaluate(self, **kwargs):
        expressions = self.values['expressions']
        return not expressions or \
                all(expressions[0].value(**kwargs) == expression.value(**kwargs)
                        for expression in expressions[1:])


class GreaterEquals(Condition):
    library = 'core'
    name = 'greater-equals'
    parameters = [
            ('left', 'expression'),
            ('right', 'expression'),
            ]

    def evaluate(self, **kwargs):
        return self.values['left'].value(**kwargs) >= \
                self.values['right'].value(**kwargs)


class Greater(Condition):
    library = 'core'
    name = 'greater'
    parameters = [
            ('left', 'expression'),
            ('right', 'expression'),
            ]

    def evaluate(self, **kwargs):
        return self.values['left'].value(**kwargs) > \
                self.values['right'].value(**kwargs)


class All(Condition):
    library = 'core'
    name = 'all'
    parameters = [
            ('condition', 'condition'),
            ]

    def evaluate(self):
        condition = self.values['condition']
        return all(condition.evaluate(player=player)
                for player in self.data.get(['players', 'list']))

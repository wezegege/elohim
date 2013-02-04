#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.action import Expression
from elohim.action.parameter import ValueParameter, GlobalData, PlayerData, ExpressionList


class Value(Expression):
    library = 'expression'
    name = 'value'
    parameters = [
            ('value', ValueParameter()),
            ]

    def value(self, **kwargs):
        return self.values['value']


class Variable(Expression):
    library = 'expression'
    name = 'variable'
    parameters = [
            ('variable', GlobalData()),
            ]

    def value(self, **kwargs):
        return self.data.get(self.values['variable'])


class PlayerVariable(Expression):
    library = 'expression'
    name = 'player-variable'
    parameters = [
            ('variable', PlayerData()),
            ]

    def value(self, **kwargs):
        if 'player' in kwargs:
            return self.data.get(self.values['variable'], kwargs['player'])
        else:
            return self.data.get(['players', 'current'] +
                    self.values['variable'])


class Sum(Expression):
    library = 'expression'
    name = 'sum'
    parameters = [
            ('expressions', ExpressionList()),
            ]

    def value(self, **kwargs):
        return sum(expression.value(**kwargs)
                for expression in self.values['expressions'])



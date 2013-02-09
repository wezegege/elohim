#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim import action
from elohim.action import parameter


class Value(action.Expression):
    library = 'expression'
    name = 'value'
    parameters = [
            ('value', parameter.ValueParameter()),
            ]

    def value(self, **kwargs):
        return self.values['value']


class Variable(action.Expression):
    library = 'expression'
    name = 'variable'
    parameters = [
            ('variable', parameter.GlobalData()),
            ]

    def value(self, **kwargs):
        return self.data.get(self.values['variable'])


class PlayerVariable(action.Expression):
    library = 'expression'
    name = 'player-variable'
    parameters = [
            ('variable', parameter.PlayerData()),
            ]

    def value(self, **kwargs):
        if 'player' in kwargs:
            return self.data.get(self.values['variable'], kwargs['player'])
        else:
            return self.data.get(['players', 'current'] +
                    self.values['variable'])


class Sum(action.Expression):
    library = 'expression'
    name = 'sum'
    parameters = [
            ('expressions', parameter.ExpressionList()),
            ]

    def value(self, **kwargs):
        return sum(expression.value(**kwargs)
                for expression in self.values['expressions'])



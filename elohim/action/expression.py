#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.action import Expression


class Value(Expression):
    library = 'core'
    name = 'value'
    parameters = [
            ('value', 'value'),
            ]

    def value(self, **kwargs):
        return self.values['value']


class Variable(Expression):
    library = 'core'
    name = 'variable'
    parameters = [
            ('variable', 'data'),
            ]

    def value(self, **kwargs):
        return self.data.get(self.values['variable'])


class PlayerVariable(Expression):
    library = 'core'
    name = 'player-variable'
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



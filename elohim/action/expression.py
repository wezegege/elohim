#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic expressions
"""

from elohim import action
from elohim.action import parameter


class Value(action.Expression):
    """A constant
    """
    library = 'expression'
    name = 'value'
    parameters = [
            ('value', parameter.ValueParameter()),
            ]

    def value(self, **_kwargs):
        return self.values['value']


class Variable(action.Expression):
    """A data tree leaf
    """
    library = 'expression'
    name = 'variable'
    parameters = [
            ('variable', parameter.GlobalData()),
            ]

    def value(self, **_kwargs):
        return self.data.get(self.values['variable'])


class PlayerVariable(action.Expression):
    """A player game data leaf
    """
    library = 'expression'
    name = 'player-variable'
    parameters = [
            ('variable', parameter.PlayerData()),
            ]

    def value(self, **kwargs):
        if 'player' in kwargs:
            player = kwargs['player']
        else:
            player = self.data.get(['players', 'current'])
        return player.get(self.values['variable'])


class Sum(action.Expression):
    """The sum of several expressions
    """
    library = 'expression'
    name = 'sum'
    parameters = [
            ('expressions', parameter.ExpressionList()),
            ]

    def value(self, **kwargs):
        return sum(expression.value(**kwargs)
                for expression in self.values['expressions'])



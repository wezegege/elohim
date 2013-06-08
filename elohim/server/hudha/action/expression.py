#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic expressions
"""

from elohim import action
from elohim.action import parameter


namespace = action.expression.namespace(__name__)


@namespace.entity('value')
class Value(action.Expression):
    """A constant
    """
    parameters = [
            ('value', parameter.ValueParameter()),
            ]

    def value(self, **_kwargs):
        return self.values['value']


@namespace.entity('variable')
class Variable(action.Expression):
    """A data tree leaf
    """
    parameters = [
            ('variable', parameter.GlobalData()),
            ]

    def value(self, **_kwargs):
        return self.data.get(self.values['variable'])


@namespace.entity('player-variable')
class PlayerVariable(action.Expression):
    """A player game data leaf
    """
    parameters = [
            ('variable', parameter.PlayerData()),
            ]

    def value(self, **kwargs):
        if 'player' in kwargs:
            player = kwargs['player']
        else:
            player = self.data.get(['players', 'current'])
        return player.get(self.values['variable'])


@namespace.entity('sum')
class Sum(action.Expression):
    """The sum of several expressions
    """
    parameters = [
            ('expressions', parameter.ExpressionList()),
            ]

    def value(self, **kwargs):
        return sum(expression.value(**kwargs)
                for expression in self.values['expressions'])



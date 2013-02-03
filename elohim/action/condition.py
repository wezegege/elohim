#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.action import Condition

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


class In(Condition):
    library = 'core'
    name = 'in'
    parameters = [
            ('element', 'expression'),
            ('list', 'expression'),
            ]

    def evaluate(self, **kwargs):
        return self.values['element'].value(**kwargs) in self.values['list'].value()

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

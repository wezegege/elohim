#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.engine.mulungu.types import Action, Condition, List, Variable
from elohim.engine.mulungu import action, param


@param('condition', Condition())
@param('actions', List(Action()))
class Foreach(Action):
  """Switch player and apply actions until condition applies
  """
  name = 'foreach'

  def play(self):
    while not self.params['condition'].applies():
      self.env.next_player()
      for action in self.params['actions']:
        action.play()


@param('condition', Condition())
@param('actions', List(Action()))
class While(Action):
  """Apply actions until condition is not met
  """
  name = 'while'

  def play(self):
    while self.params['condition'].applies():
      for action in self.params['actions']:
        action.play()


@param('condition', Condition())
@param('then', List(Action()))
@param('else', List(Action()))
class If(Action):
  """Apply "then" branch if condition is met, "else" otherwise
  """
  name = 'if'

  def play(self):
    result = 'then' if  self.params['condition'].applies() else 'else'
    for action in self.params[result]:
      action.play()


@param('source', Variable())
@param('destination', Variable())
class Add(Action):
  name = 'add'

  def play(self):
    self.params['destination'].value += self.params['source'].value

class Transfer(Add):
  name = 'transfer'

  def play(self):
    super(Transfer, self).play()
    self.params['source'].reset()

@param('variable', Variable())
class Reset(Action):
  name = 'reset'

  def play(self):
    self.params['source'].reset()

@param('variable', Variable())
@param('value', Value())
class Set(Action):
  name = 'set'

  def play(self):
    self.param['variable'].value = self.params['value']


@param('condition', Condition())
class WinnerBest(Action):
  name = 'winner_best'

  def play(self):
    pass

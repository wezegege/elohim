#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.engine.mulungu.types import Action, Condition, List, Variable
from elohim.engine.mulungu import action, param, setting
from threading import Timer, Condition

@param('fields', List(Tuple(Variable(), Type())))
@setting('timeout', Integer())
class Ask(Action):
  name = 'ask'

  def play(self):
    self.done = list()
    for variable, var_type in self['fields']:
      self.done.append(variable)
      self.env.ask(Query(variable, var_type))
    self.timer = Timer(self['timeout'], self.no_answer)
    self.waiting = Condition()
    self.waiting.acquire()
    self.waiting.wait()
    self.waiting.release()

  def no_answer(self):
    self.waiting.acquire()
    self.waiting.notify()
    self.waiting.release()

  def input(self, field):
    variable, value = field.variable, field.value
    if variable in self.done:
      self.done.remove(variable)
      self.env.set(variable, value)
      if not self.done:
        self.timer.cancel()
        self.waiting.acquire()
        self.waiting.notify()
        self.waiting.release()



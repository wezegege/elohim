#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.engine.mulungu.types import Action, Condition, List, Variable
from elohim.engine.mulungu import action, param, setting

@param('variable', Variable())
@param('type', Type())
@setting('timeout', Integer())
class Ask(Action):
  name = 'ask'

  def play(self):
    #TODO: implement this
    pass


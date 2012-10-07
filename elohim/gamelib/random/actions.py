#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.engine.mulungu.types import Action, Condition, List, Variable
from elohim.engine.mulungu import action, param

@param('destination', Variable())
@param('size', Integer())
class RollDice(Action):
  name = 'dice'

  def play(self):
    #TODO: implement this
    pass


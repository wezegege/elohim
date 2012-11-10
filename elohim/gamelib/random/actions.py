#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.engine.mulungu.types import Action, Condition, List, Variable
from elohim.engine.mulungu import action, param

import random

@param('destination', Variable())
@param('size', Integer())
class RollDice(Action):
  name = 'dice'

  def __init__(self, *args, **kwargs):
    super(RollDice, self).__init__(*args, **kwargs)
    random.seed()

  def play(self):
    result = random.randint(1, self['size'])
    self.env.set(self['destination'], result)


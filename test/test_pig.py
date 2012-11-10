#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.gamelib.core import Foreach, While, If, Add, Transfer, Reset, Set, WinnerBest
from elohim.engine.mulungu import Comparison, Enum
from elohim.gamelib.input import Ask
from elohim.gamelib.random import RollDice

from unittest2 import TestCase

class PigTest(TestCase):
  def setEngineUp(self):
    roll_if = If(
        condition=Comparison('player::current::roll::dice', '=', 1),
        then=[
          Reset('player::current::score::temporary'),
          Reset('player::current::turn'),
          ],
        else=[
          Add('player::current::roll::dice',
            'player::current::score::temporary'),
          ],
        )

    choice = If(
      condition=Comparison('player::current::move', '=', 'roll'),
      then=[
        RollDice('player::current::roll::dice', 6),
        roll_if,
        ],
      else=[
        Transfer('player::current::score::temporary',
          'player::current::score::permanent'),
        ]
      )

    rules = [
        Foreach(
        condition=Comparison('someone::permanent::score', '>=', 100),
        actions=[
          While(
            condition=Comparison('player::current::turn', '=', True),
          actions=[
            Ask( fields=[
                ('move', Enum('hold', 'roll')),
                ]),
            choice,
            ])
          ]),
        WinnerBest(variable='score::permanent'),
        ]


  def setUp(self):
    self.setEngineUp()


#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mock import Mock
from elohim.engine.isora.descriptor import describe, param, block

def test_complete_rules():
  """
  """

  @describe('It is for {players_min} '
      '(to {players_max} players|at least')
  @describe('It is for {players_max} at most')
  @param('players_min', 'integer')
  @param('players_max', 'integer')
  class PlayersMetadata(Mock):
    pass

  @describe('This game is in categories {categories}')
  @param('categories', 'list', ('string',))
  class CategoriesMetadata(Mock):
    pass

  @describe('For each player until {source} {operator} '
      '[{destination}|{integer}|{string}]')
  @param('source', 'variable')
  @param('destination', 'variable')
  @param('integer', 'integer')
  @param('string', 'string')
  @block('actions')
  class ForeachAction(Mock):
    pass

  @describe('Face player with these options :')
  @block('options', '- option {integer} :')
  class OptionAction(Mock):
    pass

  @describe('Roll a [d{size}|dice]')
  @param('size', 'integer')
  class RollAction(Mock):
    pass

  content = """
      It is for 4 players at least
      This game is in categories "dices", "gambling" and "something"
      For each player until someone's permanent score >= 100 (player-turn)
        Face player with these options :
          - option 1 :
            Roll a d8
          - option 2 :
            Roll a dice
      """


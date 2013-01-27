#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps
from pyparsing import (Word, Literal, CaselessLiteral, QuotedString, Keyword,
    Optional, OneOrMore, ZeroOrMore,
    Combine, Or, Forward,
    alphas, alphanums, nums, lineStart, lineEnd, restOfLine)

class Parameter(object):
  types = dict()

  def __call__(self, func):
    self.types[func.__name__] = func

    @wraps(func)
    def param_func(*args):
      result = func(*args)
      return result
    return param_func

parameter = Parameter()

@parameter
def integer():
  """
  >>> integer().parseString("+123")
  ([123], {})
  """
  result = Word("+-" + nums, nums)
  result.setParseAction(lambda s, l, t: int(t[0]))
  return result

@parameter
def number():
  """
  >>> number().parseString("-1.25e-2")
  ([-0.0125], {})
  """
  point = Literal(".")
  e = CaselessLiteral("e")
  result = Combine(Word("+-" + nums, nums) +
      Optional(point + Optional(Word(nums))) +
      Optional(e + Word("+-" + nums, nums)))
  result.setParseAction(lambda s, l, t: float(t[0]))
  return result

@parameter
def version():
  """
  >>> version().parseString('1.0.0.0')
  (['1.0.0.0'], {})
  >>> version().parseString('1.0.1c2.dev456')
  (['1.0.1c2.dev456'], {})
  >>> version().parseString('1.0a2')
  (['1.0a2'], {})
  >>> version().parseString('1.0rc2.1')
  (['1.0rc2.1'], {})
  >>> version().parseString('1.0b1.post456')
  (['1.0b1.post456'], {})
  >>> version().parseString('1.0.post456.dev34')
  (['1.0.post456.dev34'], {})
  """
  point = Literal(".")
  status = Literal('a') | 'b' | 'c' | 'rc'
  result = Combine(Word(nums) +
      OneOrMore(point + Word(nums)) +
      Optional(status + Word(nums) + ZeroOrMore(point + Word(nums))) +
      Optional(Literal(".post") + Word(nums)) +
      Optional(Literal(".dev") + Word(nums))
      )
  return result

@parameter
def string():
  """
  >>> string().parseString('"coucou comment ca va ?" bien ?')
  (['coucou comment ca va ?'], {})
  >>> string().parseString(r'"cou\\"cou" ""')
  (['cou"cou'], {})
  """
  result = QuotedString('"', '\\')
  return result

@parameter
def variable():
  """
  >>> variable().parseString("player's temporary score")
  (['player::score::temporary'], {})
  >>> variable().parseString("players' beginning's threat")
  (['players::beginning::threat'], {})
  >>> variable().parseString("_global temporary score")
  (['score::temporary::_global'], {})
  """
  def transform(_source, _location, tokens):
    """Transform human-style subject to namespace-like words

    Words with possessive ("'s") stay at beginning, other at the end in reverse order
    """
    begin = list()
    end = list()
    beginning = False
    for token in reversed(tokens):
      if token == "'":
        beginning = True
      elif beginning:
        begin.insert(0, token)
        beginning = False
      else:
        end.append(token)
    result = '::'.join(begin + end)
    return result
  word = Word(alphas + '_', alphanums + '-_')
  result = OneOrMore(word + Optional(Literal("'") + Optional('s').suppress()))
  result.setParseAction(transform)
  return result

@parameter
def enum(*values):
  """
  >>> enum('>', '=', '<', '>=', '<=', '!=').parseString('<')
  (['<'], {})
  """
  result = Or((Literal(value) for value in values))
  return result

@parameter
def array(value_type, *args):
  """
  >>> array('integer').parseString('12, 554, 86')
  ([([12, 554, 86], {})], {})
  """
  assert value_type in Parameter.types
  value_parser = Parameter.types.get(value_type)(*args)
  result = (value_parser + 
      ZeroOrMore(Literal(',').suppress() + value_parser) +
      Optional(Keyword('and').suppress() + value_parser))
  result.setParseAction(lambda s, l, t: [t])
  return result

def statement():
  result = None
  return result

def parser():
  statements = Forward()
  comment = lineStart + Literal('#') + Optional(restOfLine) + lineEnd
  comment.suppress()

  statements << OneOrMore(statement() | comment)


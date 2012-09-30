#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps
from pyparsing import (Literal, Keyword, Word, Combine, printables,
    And, alphanums, OneOrMore, Suppress, MatchFirst, Or)

from elohim.engine.isora.parser import Parameter

class Descriptor(object):
  def __init__(self, cls):
    self.phrases = list()
    self.parameters = dict()
    self.blocks = dict()
    self.cls = cls

  def get_parser(self):
    """
    >>> class Test(object):
    ...   def __init__(self, source, value):
    ...     self.result = {'source' : source, 'value' : value}
    ...   def __repr__(self):
    ...     return "Test(source = {source}, value = {value})".format(**self.result)
    >>> desc = Descriptor(Test)
    >>> desc.phrases = ['If {source} = {value}']
    >>> desc.parameters = {
    ...     'source' : ('variable', list()),
    ...     'value' : ('integer', list()),
    ...     }
    >>> parser = desc.get_parser()
    >>> parser.parseString("If player's score = 100")
    ([Test(source = player::score, value = 100)], {})
    """
    def handle_variable(source, location, tokens):
      assert len(tokens) == 1
      name = tokens[0]
      assert name in self.parameters
      var_type, args = self.parameters[name]
      assert var_type in Parameter.types
      parser = Parameter.types[var_type](*args).setResultsName(name)
      return parser

    def handle_keyword(source, location, tokens):
      assert len(tokens) == 1
      return Keyword(tokens[0]).suppress()

    def handle_phrase(source, location, tokens):
      def create_action(source, location, tokens):
        return self.cls(*tokens)
      return And(tokens).setParseAction(create_action)

    variable = Combine(Suppress('{') +
        Word(alphanums + '-_') +
        Suppress('}'))
    variable.setParseAction(handle_variable)
    word = Word(printables).setParseAction(handle_keyword)
    parser = OneOrMore(MatchFirst([variable, word])).setParseAction(handle_phrase)
    result = [parser.parseString(phrase) for phrase in self.phrases]
    result = [tokens[0] for tokens in result]
    result = Or(result)
    return result

def descriptor_decorator(func):
  @wraps(func)
  def decorator_func(cls):
    if not hasattr(cls, 'descriptor'):
      cls.descriptor = Descriptor(cls)
    return func(cls)
  return decorator_func

def describe(phrase):
  """
  >>> @describe('If {source} {operator} {destination}')
  ... class Action(object):
  ...   pass
  >>> Action.descriptor.phrases
  ['If {source} {operator} {destination}']
  """
  @descriptor_decorator
  def desc_func(cls):
    cls.descriptor.phrases.append(phrase)
    return cls
  return desc_func

def param(name, param_type, *args):
  """
  >>> @param('count', 'integer')
  ... @param('operator', 'enum', '>', '<', '=')
  ... class Action(object):
  ...   pass
  >>> Action.descriptor.parameters['count']
  ('integer', ())
  >>> Action.descriptor.parameters['operator']
  ('enum', ('>', '<', '='))
  """
  @descriptor_decorator
  def param_func(cls):
    cls.descriptor.parameters[name] = (param_type, args)
    return cls
  return  param_func

def block(name, phrase=None):
  """
  >>> @block('actions')
  ... @block('then', 'Then')
  ... class Action(object):
  ...   pass
  >>> Action.descriptor.blocks['actions'] is None
  True
  >>> Action.descriptor.blocks['then']
  'Then'
  """
  @descriptor_decorator
  def block_func(cls):
    cls.descriptor.blocks[name] = phrase
    return cls
  return block_func


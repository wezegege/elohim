#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps

class Descriptor(object):
  def __init__(self, cls):
    self.phrases = list()
    self.parameters = dict()
    self.blocks = dict()
    self.cls = cls

  def get_parser(self):
    return self.phrase

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


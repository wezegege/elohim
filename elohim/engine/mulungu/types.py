#!/usr/bin/env python
# -*- coding: utf-8 -*-

class EntityMcls(type):
  """
  """
  types = dict()

  def __new__(mcls, name, bases, args):
    result = type.__new__(mcls, name, bases, args)
    mcls.types[name.lower()] = result
    return result

class Entity(EntityMcls('EntityBase', (object,), {})):
  def __init__(self, env):
    self.env = env
    self.params = dict()
    self.settings = dict()
    self.state = dict()

  def __getitem__(self, name):
    for data in ('params', 'settings', 'state'):
      if name in getattr(self, data):
        return getattr(self, data)[name]
    raise KeyError()

##################################################################
# Basic types
##################################################################

class Type(Entity):
  pass

class Integer(Type):
  pass

class Number(Type):
  pass

class Version(Type):
  pass

class String(Type):
  pass

class Boolean(Type):
  pass

class Enum(Type):
  pass

##################################################################
# Advanced types
##################################################################

class Variable(Type):
  pass

@param('index', Variable())
class Pointer(Type):
  @property
  def value(self):
    return self['index'].value

##################################################################
# Containers
##################################################################

@param('type', Type())
class List(Type):
  pass

class Dictionnary(Type):
  pass

class Tuple(Type):
  pass

@param('list', Variable())
@param('unwanted', Variable())
class OtherIterator(Type):
  @property
  def value(self):
    unwanted = self['unwanted']
    iterator = self['list']
    for index in range(len(iterator)):
        if index != unwanted:
        yield iterator[index]

##################################################################
# Comparison
##################################################################

class Condition(Entity):
  def applies(self):
    return True

@param('conditions', List(Condition()))
class And(Condition):
  def applies(self):
    return all(condition.applies() for condition in self['conditions'])

@param('conditions', List(Condition()))
class Or(Condition):
  def applies(self):
    return any(condition.applies() for condition in self['conditions'])

@param('condition', Condition())
class Not(Condition):
  def appliers(self):
    return not self['condition'].applies()

@param('source', Entity())
@param('destination', Entity())
@param('operator', Operator())
class Comparison(Condition):
  def applies(self):
    return self['operator'].compute(
        self['source'],
        self['destination'])

@param('value', String())
class Operator(Entity):
  def compute(self, source, destination):
    return False

##################################################################
# Statements
##################################################################

class Action(Entity):
  def run(self):
    self.env.pause.wait()
    self.play()


  def settings(self):
    return dict(((name, value.settings())
        for name, value in self.parameters))

  def state(self):
    return None

  def load_state(self, _state):
    pass

class Metadata(Entity):
  pass

class Message(Entity):
  pass

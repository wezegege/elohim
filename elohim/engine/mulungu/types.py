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

##################################################################
# Basic types
##################################################################

class Integer(Entity):
  pass

class Number(Entity):
  pass

class Version(Entity):
  pass

class String(Entity):
  pass

class Boolean(Entity):
  pass

##################################################################
# Advanced types
##################################################################

class Variable(Entity):
  pass

class Enum(Entity):
  pass

class Type(Entity):
  pass

##################################################################
# Containers
##################################################################

@param('type', Type())
class List(Entity):
  pass

class Tuple(Entity):
  pass

##################################################################
# Comparison
##################################################################

class Condition(Entity):
  def applies(self):
    return True

@param('conditions', List(Condition()))
class And(Condition):
  def applies(self):
    return all(condition.applies() for condition in self.params['conditions'])

@param('conditions', List(Condition()))
class Or(Condition):
  def applies(self):
    return any(condition.applies() for condition in self.params['conditions'])

@param('condition', Condition())
class Not(Condition):
  def appliers(self):
    return not self.params['condition'].applies()

@param('source', Entity())
@param('destination', Entity())
@param('operator', Operator())
class Comparison(Condition):
  def applies(self):
    return self.params['operator'].compute(
        self.params['source'],
        self.params['destination'])

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

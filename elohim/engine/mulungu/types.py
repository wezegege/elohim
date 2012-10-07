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

Entity = EntityMcls('Entity', (object,), {})

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

class List(Entity):
  pass

class Tuple(Entity):
  pass

##################################################################
# Comparison
##################################################################

class Condition(Entity):
  pass

class And(Entity):
  pass

class Or(Entity):
  pass

class Operator(Entity):
  pass

##################################################################
# Statements
##################################################################

class Action(Entity):
  pass

class Metadata(Entity):
  pass

class Message(Entity):
  pass

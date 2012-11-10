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

class VarDict(Entity):
    def __init__(self):
        super(VarDict, self).__init__()
        self.values = dict()

    def get(self, item):
        pass

    def set(self, item, value):
        pass

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

def entity_list(name, bases, attrs):
  attrs['logger'] = logging.getLogger(name)
  result = type(name, bases, attrs)
  result.items[name.lower()] = result
  return result

EntityList = entity_list('EntityList', (object,), dict())

class Entity(EntityList):
  entity_type = ('parameters', 'controllers', 'views', 'children')
  items = dict()

  def __init__(self, *args, **kwargs):
    pass

  def require(self):
    return list()

  def info(self):
    result = {
        'type' : self.__class__.__name__,
        }
    for item in self.entity_types:
      result[item] = [entity.info() for entity in getattr(self, item)]
    return result

  @classmethod
  def from_info(cls, info):
    entity = self.items.get(info.get('type', '').lower(), cls)
    result = entity()
    for item in self.entity_types:
      if item in info:
        setattr(cls, item, [cls.from_info(sample) for sample in info[item])
    return result


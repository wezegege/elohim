#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Signal(object):
  def __init__(self):
    self.slots = list()

  def connect(self, func):
    assert callable(func)
    self.slots.append(func)

  def __call__(self, *args, **kwargs):
    for slot in self.slots:
      slot(*args, **kwargs)

class Parameter(object):
  def __init__(self, defaultValue):
    self.changed = Signal()
    self.value = defaultValue

  def get(self):
    return self.value

  def set(self, value):
    self.value = value
    self.changed()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hud import Entity

class Parameter(Entity):
  def __init__(self, value=None):
    self.value = value

  def __call__(self):
    return self.value

  def set(self, value):
    self.value = value

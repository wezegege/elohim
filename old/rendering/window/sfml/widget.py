#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

def compute_position(widget):
  params = widget.parameters['position']
  result = (0, 0)
  if params['relative-position'] and widget.parent:
    origin = widget.parent.get('position')
  else:
    origin = widget.window.get('position')
  for index in range(2):
    if params['base-position'][index]:
      result[index] = (origin[index] +
          params['base-position'][index] -
          center[index])
    else:
      if params['pin'][index]

class Widget(object):

  defaults = {
      'general' : {
        'name' : lambda: None,
        'id' : lambda: None,
        'class' : lambda: list(),
        'display' : lambda: True,
        'enabled' : lambda: True,
        },

      'position' : {
        'base-position': lambda: (None, None),
        'relative-position' : lambda: False,
        'origin' : lambda: (0, 0),
        'center' : lambda: (0, 0),
        'pin' : lambda: (None, None),
        # left, center, right
        # top, center, bottom
        },

      'size' : {
        'base-size' : lambda: (None, None),
        'min-size' : lambda: None,
        'max-size' : lambda: None,

        'scale' : lambda: None,
        'min-scale' : lambda: None,
        'max-scale' : lambda: None,
        'fill' : lambda: False,
        },

      'layout' : {
        'float' : lambda: None, #vertical, horizontal
        'align' : lambda: None, #right, center, left, top, bottom
        'float-reverse' : lambda: False,
        'float-base' : lambda: (None, None),
        # left, center, right
        # top, center, bottom
        },
      }

  def __init__(self, *args, **kwargs):
    """@todo: to be defined """
    self.logger = logging.getLogger(self.__class__.__name__)
    self.parent = kwargs.get('parent', None)
    self.children = list()
    self.controllers = list()
    self.views = list()
    self.parameters = {
        key : kwargs.get(key, category[key]())
        for category in self.defaults.values()
        for key in category.keys()
        }
    self.changes = {
        key : True for key in self.defaults.keys()
        }

  def get(self, name):
    if name in self.parameters:
      self.parameters.get(name).value

  def set(self, name, value):
    if name in self.parameters:
      self.parameters[name] = value
      category = next(key for key, value in self.defaults.items()
          if name in value.keys())
      self.changes[category] = True

  def handle(self, context):
    for controller in self.controllers:
      controller.handle(context)
    for child in self.children:
      child.handle(context)

  def render(self, window):
    for view in self.views:
      for surface in view.render():
        window.Draw(surface)
    for child in self.children:
      child.render(window)


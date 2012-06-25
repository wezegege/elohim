#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hud import Entity

class Widget(Entity):

  def __init__(self, *args, **kwargs):
    """@todo: to be defined """
    self.logger = logging.getLogger(self.__class__.__name)
    self.parent = kwargs.get(parent, None)
    self.parameters = list()
    self.children = list()
    self.controllers = list()
    self.views = list()

  def __getattr__(self, name):
    if name in self.parameters:
      self.parameters.get(name).value
    else:
      super(Widget, self).__getattr__(name)

  def __setattr__(self, name, value):
    if name in self.parameters:
      self.parameters.get(name).set(value)
    else:
      super(Widget, self).__setattr__(name, value)

  def handle(self, event):
    for controller in self.controllers:
      controller.handle(event)
    for child in self.children:
      child.handle(event)

  def render(self, window):
    for view in self.views:
      for surface in view.render():
        window.Draw(surface)
    for child in self.children:
      child.render(window)


#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Widget(object):
  """Docstring for Widget """

  def __init__(self, **kwargs):
    """@todo: to be defined """
    self.logger = logging.getLogger(self.__class__.__name)
    self.children = list()
    self.parent = kwargs.get(parent, None)
    self.parameters = dict()
    self.surfaces = list()
    self.eventHandlers = list()
    self.renderers = list()
    self.computers = list()

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

  def handleEvent(self, event):
    for handler in self.eventHandlers:
      handler.handle(event)
    for child in self.children:
      child.handleEvent(event)

  def compute(self):
    for computer in self.computers:
      computer.compute()
    for child in self.children:
      child.compute()

  def render(self, window):
    for renderer in self.renderers:
      renderer.render()
    for surface in self.surfaces:
      window.Draw(surface)
    for child in self.children:
      child.draw(window)


#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySFMl import sf
import logging

class Window(object):
  logger = logging.getLogger('Window')

  def __init__(self, **kwargs):
    self.window = None
    for param, default in (
        ('widgets',  dict()),
        ('framerate', 60),
        ('title', 'Pokertemplate'),
        ('vsync', True),
        ):
      setattr(self, param, kwargs.get(param, default))


#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.utils.metrics import loophandlers

import sfml
import time


class Window(object):

    width = 180
    height = width  * 3 / 4
    scale = 3
    name = "Game"

    def __init__(self, loophandler=None):
        self.window = sfml.RenderWindow(
                sfml.VideoMode(self.width * self.scale,
                    self.height * self.scale),
                self.name)
        self.loophandler = loophandlers.LoopHandler() \
                if loophandler is None else loophandler

    def render(self):
        self.window.clear()
        self.window.display()

    def handle_events(self):
        for event in self.window.events:
            if isinstance(event, sfml.CloseEvent):
                self.window.close()

    def compute(self):
        pass

    def run(self):
        while self.window.is_open:
            with self.loophandler:
                self.handle_events()
                self.compute()
                self.render()


if __name__ == '__main__':
    window = Window()
    window.run()


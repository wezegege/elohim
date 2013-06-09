#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time


class NoPacer(object):
    def pace(self, _duration):
        pass


class Pacer(object):
    def __init__(self, rate=60):
        self.tick = 1 / rate

    def pace(self, duration):
        to_sleep = self.tick - duration
        if to_sleep > 0:
            time.sleep(to_sleep)


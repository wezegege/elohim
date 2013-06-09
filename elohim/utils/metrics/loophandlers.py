#!/usr/bin/env python
# -*- coding: utf-8 -*-


from elohim.utils.metrics import raters, pacers


class LoopHandler(object):
    def __init__(self, rater=None, pacer=None):
        self.timestamp = 0
        self.rater = raters.FastFramerate() \
                if rater is None else rater
        self.pacer = pacers.NoPacer() \
                if pacer is None else pacer

    def __enter__(self):
        self.timestamp = time.time()
        self.rater.tick(self.timestamp)

    def __exit__(self, exc_type, exc_value, traceback):
        timestamp = time.time()
        duration = timestamp - self.timestamp
        self.pacer.pace(duration)



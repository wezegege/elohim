#!/usr/bin/env python
# -*- coding: utf-8 -*-


from elohim.client.ui.njord import framerate as framerates, timer as timers

class Pacer(object):
    refresh_rate = 60

    def __init__(self, framerate=None, timer=None):
        self.tick = 1 / self.refresh_rate
        self.timestamp = 0
        self.framerate = framerates.FastFramerate() \
                if framerate is None else framerate
        self.timer = timers.Timer() if timer is None else timer

    def __enter__(self):
        timestamp = self.timer.time()
        self.framerate.tick(timestamp)
        self.timestamp = timestamp

    def __exit__(self, exc_type, exc_value, traceback):
        timestamp = self.timer.time()
        to_sleep = self.tick - timestamp + self.timestamp
        if to_sleep > 0:
            self.timer.sleep(to_sleep)



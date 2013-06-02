#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sfml


class Timer(object):
    def time(self):
        return time.time()

    def sleep(self, amount):
        time.sleep(amount)


class SFMLTimer(object):
    def time(self):
        return time.time()

    def sleep(self, amount):
        sfml.sleep(sfml.seconds(amount))


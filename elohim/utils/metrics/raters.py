#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Rater(object):
    def __init__(self):
        self.last_tick = 0
        self.last_rate = 0

    def tick(self, timestamp):
        self.last_rate = self.compute(timestamp)

    def compute(self, timestamp):
        result = 1 / (timestamp - self.last_tick)
        self.last_tick = timestamp
        return result

    def value(self):
        return self.last_rate


class FastRater(Rater):
    def __init__(self, ratio=0.9):
        super().__init__()
        self.ratio = ratio
        self.reverted_ratio = 1 - ratio

    def tick(self, timestamp):
        rate = self.compute(timestamp)
        smoothed_rate = self.ratio * rate + \
                self.reverted_ratio * self.last_rate
        self.last_rate = smoothed_rate


class SampleRater(Rater):
    DEFAULT_SAMPLES = 100

    def __init__(self, samples = DEFAULT_SAMPLES):
        super().__init__()
        self.max_samples = samples
        self.rates = [0] * self.max_samples
        self.index = 0
        self.rate_sum = 0

    def tick(self, timestamp):
        rate = self.compute(timestamp)
        self.rate_sum += rate
        self.rate_sum -= self.rates[self.index]
        self.rates[self.index] = rate
        self.index += 1
        if self.index >= self.max_samples:
            self.index = 0

    def value(self):
        return self.rate_sum / self.max_samples


class DerivativeRater(Rater):
    def __init__(self, limit=100):
        super().__init__()
        self.limit = limit
        self.index = 0

    def tick(self, timestamp):
        duration = timestamp - self.last_tick
        dividende = duration * self.last_rate + self.index - 1
        if dividende:
            result = self.index * self.last_rate / dividende
        else:
            result = 1 / duration
        self.last_rate = result
        self.last_tick = timestamp
        if self.index < self.limit:
            self.index += 1


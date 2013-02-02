#!/usr/bin/env python
# -*- coding: utf-8 -*-

class GameFabric(object):
    actions = dict()

    @classmethod
    def make_library(cls, title):
        cls.actions[title] = dict()
        def register(name):
            def make_register(action):
                cls.actions[title][name] = action
                return action
            return make_register
        return register

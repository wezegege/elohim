#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Namespace(object):

    def __init__(self):
        self.entities = dict()
        self.namespaces = dict()

    def namespace(self, name):
        result =  Namespace()
        self.namespaces[name] = result
        return result

    def entity(self, name):
        def wrapped_function(cls):
            self.entities[name] = cls
            return cls
        return wrapped_function()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy


class Visibility(object):
    class All(object):
        pass

    class Player(object):
        pass

    class TeamMembers(object):
        pass

    class Opponents(object):
        pass

    class Nobody(object):
        pass

def operation(func):
    def wrapper(self, index, *args, **kwargs):
        if self.reference:
            return getattr(self.reference(self.root), func.__name__)(index, *args, **kwargs)
        elif index:
            index = copy.copy(index)
            entry = index.pop(0)
            return getattr(self.getitem(entry), func.__name__)(index, *args, **kwargs)
        else:
            return func(self, *args, **kwargs)
    return wrapper


class Entry(object):
    class Unset(object):
        pass

    def __init__(self, **kwargs):
        self.reference = kwargs.get('reference', None)
        self.root = kwargs.get('root', self)
        self.content = kwargs.get('content', self.Unset)
        self.default = kwargs.get('default', self.Unset)
        self.visibility = kwargs.get('visibility', Visibility.All)
        self.subentries = dict()

    def initialize(self):
        if self.reference:
            self.reference(self.root).initialize()
        else:
            if not self.default is self.Unset:
                self.content = self.default
            for field, entry in self.subentries.items():
                entry.initialize()

    @operation
    def refer(self, reference):
        self.reference = reference

    @operation
    def configure(self, **kwargs):
        for field, value in kwargs.items():
            if hasattr(self, field):
                setattr(self, field, value)
            else:
                raise AttributeError()

    @operation
    def get(self):
        if self.content is self.Unset:
            return self
        else:
            return self.content

    @operation
    def add(self, value):
        self.content += value
        return value

    @operation
    def set(self, value):
        self.content = value
        return value

    def getitem(self, field):
        if self.reference is None:
            return self.subentries.setdefault(field, Entry(root=self.root))
        else:
            return self.reference(self.root).getitem(field)

    def __iter__(self):
        for value in self.subentries.values():
            yield value

    def __contains__(self, value):
        return value in self.subentries

    def __repr__(self):
        if self.reference is not None:
            return repr(self.reference(self.root))
        elif self.content is not self.Unset:
            return repr(self.content)
        else:
            return repr(self.subentries)



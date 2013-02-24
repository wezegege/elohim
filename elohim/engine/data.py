#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import re


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


def operation(strict=True):
    def decorator(func):
        def wrapper(self, index, *args, **kwargs):
            if self.reference:
                return getattr(self.reference(self.root), func.__name__)(index, *args, **kwargs)
            elif index:
                index = copy.copy(index)
                entry = index.pop(0)
                return getattr(self.getitem(entry, strict), func.__name__)(index, *args, **kwargs)
            else:
                return func(self, *args, **kwargs)
        return wrapper
    return decorator


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
        if not self.reference:
            if not self.default is self.Unset:
                self.content = self.default
            for field, entry in self.subentries.items():
                entry.initialize()

    @operation(strict=False)
    def refer(self, reference):
        self.reference = parse_pointer(reference)

    @operation(strict=False)
    def configure(self, **kwargs):
        for field, value in kwargs.items():
            if hasattr(self, field):
                setattr(self, field, value)
            else:
                raise AttributeError()

    @operation()
    def reset(self):
        if not self.default is self.Unset:
            self.content = self.default

    @operation()
    def get(self):
        return self.doget()

    @operation(strict=False)
    def getdefault(self):
        return self.doget()

    def doget(self):
        if self.content is self.Unset:
            return self
        else:
            return self.content

    @operation()
    def add(self, value):
        self.content += value
        return value

    @operation(strict=False)
    def set(self, value):
        self.content = value
        return value

    def getitem(self, field, strict=True):
        if self.reference is None:
            if strict and not field in self.subentries:
                raise KeyError
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
            return repr(self.reference)
        elif self.content is not self.Unset:
            return repr(self.content)
        else:
            return repr(self.subentries)


def parse_pointer(reference):
    class Word(object):
        def __init__(self, word):
            self.word = word

        def __call__(self, _root):
            return self.word

        def __repr__(self):
            return self.word

        def __str__(self):
            return self.word

    class Reference(object):
        def __init__(self, words):
            self.words = words

        def __call__(self, root):
            return root.get([word(root) for word in self.words])

        def __repr__(self):
            return repr(self.words)

        def __str__(self):
            return '<{words}>'.format(words='::'.join(str(word) for word in self.words))

    tokens = re.findall('[\w\d_-]+|[<>]', reference)

    def parse(tokens):
        result = list()
        while tokens:
            token = tokens.pop(0)
            if token == '<':
                result.append(parse(tokens))
            elif token == '>':
                break
            else:
                result.append(Word(token))
        return Reference(result)

    return parse(tokens)


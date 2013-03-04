#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module handling the different informations for a game to occur
"""

import copy
import re
import functools


class Visibility(object):
    """Handle whether the different players and spectators will see
    a given information
    """
    class All(object):
        """Everyone will see the information
        """
        pass

    class Player(object):
        """Only owner player will see the information
        """
        pass

    class TeamMembers(object):
        """Only owner player and the members of his team will see
        """
        pass

    class Opponents(object):
        """Only opponents of owner player will see
        """
        pass

    class Nobody(object):
        """No one can see the information
        """
        pass


def operation(strict=True):
    """Decorator to handle the entries as a tree.

    Entries are seen as a tree, and the goal entry is designated
    with a list of keys. This decorator assures the finding of
    the good entry before the operation is done
    """
    def decorator(func):
        """The actual decorator with a parameter `strict`
        """
        @functools.wraps(func)
        def wrapper(self, index, *args, **kwargs):
            """Wrapper function to be used instead of original one
            """
            if self.reference:
                result = getattr(self.pointee,
                        func.__name__)(index, *args, **kwargs)
            elif index:
                index = copy.copy(index)
                entry = index.pop(0)
                result = getattr(self.getitem(entry, strict),
                        func.__name__)(index, *args, **kwargs)
            else:
                result = func(self, *args, **kwargs)
            return result
        return wrapper
    return decorator


def modifier(func):
    """Decorator to mark a method which implies changes to data

    An entry can be subscribed to, in which case whenever a change
    is made to this entry, all subscribers are notified.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        """Wrapper function to be used instead of original one
        """
        old = self.content
        result = func(self, *args, **kwargs)
        if old != self.content:
            for condition, handler in self.handlers:
                if condition(self.content):
                    handler(self.content)
        return result
    return wrapper


class Entry(object):
    """Node of a tree handling a piece of information.

    An entry has a notion of subentries, which correspond to branches,
    and of pointer : an entry may refer to another entry, so when
    this entry is used, all methods will be delegated to the pointee.
    """
    Unset = type('Unset', (object,), dict())

    def __init__(self, **kwargs):
        """

        All parameters are optional.

        :param reference: a string representing the entry this one is
            referring to. Default : None
        :param root: the root of the entry tree. Default : self
        :param content: the value for this entry. Default : Unset
        :param default: a default value for this entry, for when it is
            resetted. Default : Unset
        :param visibility: the visibility of the entry, controlling
            whether a player or a spectator can have access to it.
            Default : All
        """
        self.reference = kwargs.get('reference', None)
        self.root = kwargs.get('root', self)
        self.content = kwargs.get('content', self.Unset)
        self.default = kwargs.get('default', self.Unset)
        self.visibility = kwargs.get('visibility', Visibility.All)
        self.subentries = dict()
        self.handlers = list()
        self.pointee = None

    @modifier
    def initialize(self):
        """Set content to default value, and ask all subentries to do so
        """
        if not self.reference:
            if not self.default is self.Unset:
                self.content = self.default
            for _, entry in self.subentries.items():
                entry.initialize()

    @operation(strict=False)
    def refer(self, reference):
        """Ask this entry to refer to another

        Also add a handler to modifiers of the reference, to be
        responsive whenever the referee changes.

        :param reference: entry to refer to
        """
        self.reference = parse_pointer(reference)
        for pointer in self.reference.modifiers():
            self.root.add_handler(pointer, lambda _ : True,
                    self.update_pointee)
        self.update_pointee(None)

    def update_pointee(self, _value):
        """Callback method to whenever the referee may have changed
        """
        try:
            self.pointee = self.reference(self.root)
        except KeyError:
            self.pointee = None

    @operation()
    def add_handler(self, condition, handler):
        """Add a function which will be called whenever the content
        of this entry changes
        """
        self.handlers.append((condition, handler))

    @operation(strict=False)
    def configure(self, **kwargs):
        """Change settings for this entry, like the default value, or
        the visibility
        """
        for field, value in kwargs.items():
            if hasattr(self, field):
                setattr(self, field, value)
            else:
                raise AttributeError()

    @operation()
    @modifier
    def reset(self):
        """Set the content to default value
        """
        if not self.default is self.Unset:
            self.content = self.default

    @operation()
    def get(self):
        """Get the value of the entry. Raise an error if entry does
        not exist
        """
        return self.doget()

    @operation(strict=False)
    def getdefault(self):
        """Get the value of the entry. Create an entry if does not exist
        """
        return self.doget()

    def doget(self):
        """The actual get method. Return the entry value if exists,
        or else the entry itself
        """
        if self.content is self.Unset:
            return self
        else:
            return self.content

    @operation(strict=False)
    def getentry(self):
        return self

    @operation()
    @modifier
    def add(self, value):
        """Add `value` to current content
        """
        self.content += value
        return value

    @operation(strict=False)
    @modifier
    def set(self, value):
        """Set content to `value`
        """
        self.content = value
        return value

    def getitem(self, field, strict=True):
        """Retrieve a subentry by its name

        Redirects to the pointee if there is one
        """
        if self.reference is None:
            if strict and not field in self.subentries:
                raise KeyError
            return self.subentries.setdefault(field, Entry(root=self.root))
        else:
            return self.pointee.getitem(field)

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
    """Take a pointer-syntax like string, and return a reference object

    reference := field | reference :: field
    field := word | < reference >
    """
    class Word(object):
        """A word in pointer grammar

        Corresponds to a field for an entry
        """
        def __init__(self, word):
            self.word = word

        def __call__(self, _root, top=None):
            return self.word

        def __repr__(self):
            return self.word

        def __str__(self):
            return self.word

    class Reference(object):
        """A reference to another entry in the data tree
        """
        def __init__(self, words):
            self.words = words

        def __call__(self, root, top=True):
            field = [word(root, top=False) for word in self.words]
            return root.getentry(field) if top else root.get(field)

        def __repr__(self):
            return repr(self.words)

        def modifiers(self, top=True):
            """Compute modifiers of a pointer

            A modifier is an entry in the data tree which value may
            change which entry is pointed by this reference
            """
            if all(isinstance(word, Word) for word in self.words):
                if not top:
                    yield [str(word) for word in self.words]
            else:
                for word in self.words:
                    if isinstance(word, Reference):
                        for entry in word.modifiers(top=False):
                            yield entry

        def __str__(self):
            return '<{words}>'.format(words='::'.join(str(word)
                for word in self.words))

    tokens = re.findall(r'[\w\d_-]+|[<>]', reference)

    def parse(tokens):
        """read the tokens of the string representation, then match
        the grammar to return a Reference object
        """
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


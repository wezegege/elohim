#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pokertemplate.engine.isora.var_types import types

class Descriptor(object):

  descriptors = list()

  def __init__(self, action, sentences, parameters=None, blocks=None):
    self.action = action
    self.sentences = sentences
    if not parameters:
      parameters = dict()
    self.parameters = dict()
    for name, param_type in parameters:
      if isinstance(param_type, tuple):
        param_type, args = param_type
      else:
        args = list()
      assert param_type in types
      self.parameters[name] = types[param_type](*args)
    self.param_dict = dict((
        (name, '(?P<{name}>{value})'.format(name=name, value=param_type.pattern))
        for name, param_type in self.parameters))
    self.blocks = blocks if blocks else list()

  @classmethod
  def register(cls, desc):
    assert desc not in cls.descriptors
    cls.descriptors.append(desc)

  @classmethod
  def from_desc(cls, content):
    for descriptor in descriptors:
      result = descriptor.match(content)
      if result:
        return result
    assert False

  def match(self, block):
    header = block.split('\n', 1)[0]
    for sentence in sentences:
      match = re.search('{sentence}(?: \((?<message>\S+)\)'.format(
        sentence=sentence.format(**self.param_dict)), header)
      if match:
        return self.desc_to_obj(self, block, match)
    return None

  def to_obj(self, block, match):
    params = dict((
      (name, self.parameters[name].transform(value))
      for name, value in match.groupdict()))
    return self.action(**params)

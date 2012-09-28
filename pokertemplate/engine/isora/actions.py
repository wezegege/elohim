#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pokertemplate.engine.isora.var_types import types

class Descriptor(object):

  descriptors = list()

  def __init__(self, action, sentences, parameters=None, blocks=None):
    """
    >>> desc = Descriptor(
    ...     action=object(),
    ...     sentences=[r'If {source} {operator} {destination}',
    ...       r'If {source} {operator} {value}'],
    ...     parameters={
    ...       'source': 'variable',
    ...       'operator' : ('enum', ('=', '<', '>')),
    ...       'destination' : 'variable',
    ...       'value' : 'int-or-string',
    ...       },
    ...     blocks='actions')
    >>> desc = Descriptor(
    ...     action=object(),
    ...     sentences=r'End turn')
    """
    self.action = action
    if isinstance(sentences, str):
      sentences = [sentences]
    self.sentences = sentences
    if not parameters:
      parameters = dict()
    self.parameters = dict()
    for name, param_type in parameters.items():
      if isinstance(param_type, tuple):
        param_type, args = param_type
      else:
        args = list()
      assert param_type in types
      self.parameters[name] = types[param_type](*args)
    self.param_dict = dict((
        (name, '(?P<{name}>{value})'.format(name=name, value=param_type.pattern))
        for name, param_type in self.parameters.items()))
    if not blocks:
      blocks = list()
    elif isinstance(blocks, (str)):
      blocks = [blocks]
    self.blocks = blocks
    self.descriptors.append(self)

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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

types = dict()

def object_type(cls):
  """
  >>> @object_type
  ... class Test(object):
  ...   name = 'something'
  >>> ('something', Test) in types.items()
  True
  >>> hasattr(Test, 'types')
  True
  """
  global types
  if hasattr(cls, 'name'):
    assert not cls.name in types
    types[cls.name] = cls
    cls.types = types
  return cls

@object_type
class Variable(object):
  """
  >>> 'variable' in types
  True
  >>> variable = Variable()
  >>> bool(re.match(variable.pattern, "player's temporary score", re.VERBOSE))
  True
  >>> result = re.search(variable.pattern, "player's temporary score", re.VERBOSE)
  >>> result.group(0)
  "player's temporary score"
  >>> variable.transform(result.group(0))
  'player:score:temporary'
  """

  name = 'variable'
  pattern = r"""
        \w[\w\d_-]+       # variable name
        (?:'s?)?          # possession
        (?:               # other names
          \s+\w[\w\d_-]+
          (?:'s?)?
        )*
      """

  def transform(self, content):
    """
    >>> variable = Variable()
    >>> variable.transform("player's dice roll")
    'player:roll:dice'
    >>> variable.transform("players' beginning's threat")
    'players:beginning:threat'
    >>> variable.transform("global temporary score")
    'score:temporary:global'
    """
    names = content.split(' ')
    end = [name for name in reversed(names)
        if not name.endswith(("'s", "'"))]
    begin = [name.rsplit("'", 1)[0]for name in names
        if not name in end]
    result = ':'.join(begin + end)
    return result

@object_type
class Integer(object):
  """
  >>> 'int' in types
  True
  >>> integer = Integer()
  >>> bool(re.match(integer.pattern, "1234", re.VERBOSE))
  True
  >>> result = re.search(integer.pattern, "6465", re.VERBOSE)
  >>> result.group(0)
  '6465'
  >>> integer.transform(result.group(0))
  6465
  """

  name = 'int'
  pattern = r"\d+"

  def transform(self, content):
    """
    >>> integer = Integer()
    >>> integer.transform("1234")
    1234
    """
    return int(content)

@object_type
class String(object):
  """
  >>> 'string' in types
  True
  >>> string = String()
  >>> bool(re.match(string.pattern, '"dice"', re.VERBOSE))
  True
  >>> result = re.search(string.pattern, '"dice"', re.VERBOSE)
  >>> result.group(0)
  '"dice"'
  >>> string.transform(result.group(0))
  'dice'
  """

  name = 'string'
  pattern = r'".+"'

  def transform(self, content):
    """
    >>> string = String()
    >>> string.transform('"dice"')
    'dice'
    """
    return content.strip()[1:-1]

@object_type
class List(object):
  """
  >>> 'list' in types
  True
  >>> stringlist = List('string')
  >>> bool(re.match(stringlist.pattern, '"dice", "gambling", "cards"', re.VERBOSE))
  True
  >>> result = re.search(stringlist.pattern, '"dice", "gambling", "cards"', re.VERBOSE)
  >>> result.group(0)
  '"dice", "gambling", "cards"'
  >>> stringlist.transform(result.group(0))
  ['dice', 'gambling', 'cards']
  """
  name = 'list'

  @property
  def pattern(self):
    """
    >>> stringlist = List('string')
    >>> stringlist.pattern
    '\\n          ".+"           # first element\\n          (?:,".+")*   # following elements\\n        '
    """
    result = r"""
          {element}           # first element
          (?:,{element})*   # following elements
        """.format(element=self.element.pattern)
    return result

  def __init__(self, element_name, *args):
    global types
    assert element_name in types
    self.element = types[element_name](*args)

  def transform(self, content):
    """
    >>> List('string').transform('"dice", "gambling", "cards"')
    ['dice', 'gambling', 'cards']
    >>> List('string').transform('"dice"')
    ['dice']
    """
    return [self.element.transform(name) for name in content.split(',') if name]

@object_type
class Enum(object):
  """
  >>> 'enum' in types
  True
  >>> enum = Enum(a='test', b='test', c='coucou')
  >>> bool(re.match(enum.pattern, "c", re.VERBOSE))
  True
  >>> result = re.search(enum.pattern, "b", re.VERBOSE)
  >>> result.group(0)
  'b'
  >>> enum.transform(result.group(0))
  'test'
  """

  name = 'enum'

  def __init__(self, *args, **kwargs):
    """
    >>> enum = Enum('a', 'b', 'c')
    >>> enum.values
    {'a': 'a', 'c': 'c', 'b': 'b'}
    >>> enum = Enum(('a', 'b', 'c'))
    >>> enum.values
    {'a': 'a', 'c': 'c', 'b': 'b'}
    >>> enum = Enum(a='test', b='test', c='coucou')
    >>> enum.values
    {'a': 'test', 'c': 'coucou', 'b': 'test'}
    >>> enum = Enum({'a':'test', 'b':'test', 'c':'coucou'})
    >>> enum.values
    {'a': 'test', 'c': 'coucou', 'b': 'test'}
    >>> enum = Enum('a')
    >>> enum.values
    {'a': 'a'}
    """
    if args:
      if len(args) == 1:
        values = args[0]
        if isinstance(values, (list, tuple)):
          self.values = dict((
            (value, value) for value in values))
        elif isinstance(values, dict):
          self.values = values
        else:
          self.values = {values: values}
      else:
        self.values = dict((
          (value, value) for value in args))
    else:
      self.values = kwargs

  @property
  def pattern(self):
    """
    >>> enum = Enum('a', 'b', 'c')
    >>> enum.pattern
    'a|c|b'
    """
    result = '|'.join((re.escape(element) for element in self.values))
    return result

  def transform(self, content):
    """
    >>> enum = Enum('=', '>', '>=', '<', '<=', '!=')
    >>> enum.transform('<=')
    '<='
    >>> dictenum = Enum(a='test', b='test', c='coucou')
    >>> dictenum.transform('b')
    'test'
    """
    assert content in self.values
    return self.values[content]

@object_type
class IntOrString(object):
  """
  >>> 'int-or-string' in types
  True
  >>> intstr = IntOrString()
  >>> bool(re.match(intstr.pattern, "1234", re.VERBOSE))
  True
  >>> result = re.search(intstr.pattern, "6465", re.VERBOSE)
  >>> result.group(0)
  '6465'
  >>> intstr.transform(result.group(0))
  6465
  >>> result = re.search(intstr.pattern, '"coucou"', re.VERBOSE)
  >>> result.group(0)
  '"coucou"'
  >>> intstr.transform(result.group(0))
  'coucou'
  """

  name = 'int-or-string'
  pattern = r'".+"|\d+'

  def transform(self, content):
    """
    >>> intstr = IntOrString()
    >>> intstr.transform("1234")
    1234
    >>> intstr.transform('"coucou"')
    'coucou'
    """
    content = content.strip()
    if content.startswith('"') and content.endswith('"'):
      return content[1:-1]
    else:
      return int(content)

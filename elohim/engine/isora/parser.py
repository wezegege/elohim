#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from pyparsing import (Word, Literal, CaselessLiteral, Regex,
    Optional,
    Combine,
    nums)

class Type(object):
  """
  >>> Type.integer.parseString("123")
  ([123], {})
  >>> Type.number.parseString("-1.25e-2")
  ([-0.0125], {})
  >>> Type.version.parseString('1.0.0.0')
  (['1.0.0.0'], {})
  >>> Type.version.parseString('1.0.1a2.dev456')
  (['1.0.1a2.dev456'], {})
  >>> Type.version.parseString('1.0a2')
  (['1.0a2'], {})
  >>> Type.version.parseString('1.0a2.1')
  (['1.0a2.1'], {})
  >>> Type.version.parseString('1.0b1.dev456')
  (['1.0b1.dev456'], {})
  >>> Type.version.parseString('1.0.post456.dev34')
  (['1.0.post456.dev34'], {})
  """
  integer = Word("+-" + nums, nums)
  integer.setParseAction(lambda s, l, t: int(t[0]))

  point = Literal(".")
  e = CaselessLiteral("e")
  number = Combine(Word("+-" + nums, nums) +
      Optional(point + Optional(Word(nums))) +
      Optional(e + Word("+-" + nums, nums)))
  number.setParseAction(lambda s, l, t: float(t[0]))

  version_pattern = r"""
      \d+(?:\.\d+)+
      (?:(?:a|b|c|rc)\d+(?:\.\d+)*)?
      (?:\.post\d+)?
      (?:\.dev\d+)?
      """
  version = Regex(version_pattern, re.VERBOSE)

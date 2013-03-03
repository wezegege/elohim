#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import unittest2

class BaseClass(object):
    pass


class TestClasses(unittest2.TestCase):
    def test_list_subclasses(self):
        subclasses = list_subclasses(BaseClass, __name__, __path__)
        class_names = (subclass.__name__ for subclass in subclasses)
        expected = ('SubclassA', 'SubclassB', 'SubclassC')
        self.assertSequenceEqual(expected, class_names)


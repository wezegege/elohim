#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.utils import classes
from elohim.utils import test

import os.path
import unittest2


class BaseClass(object):
    pass


class TestClasses(unittest2.TestCase):
    def test_list_subclasses(self):
        subclasses = classes.list_subclasses(BaseClass, test.__name__, test.__path__)
        class_names = [subclass.__name__ for subclass in subclasses]
        for expected in ('SubclassA', 'SubclassB', 'SubclassC'):
            self.assertIn(expected, class_names)


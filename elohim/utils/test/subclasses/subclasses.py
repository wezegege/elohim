#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.utils.test.test_classes import BaseClass

class SubclassA(BaseClass):
    pass

class SubclassB(BaseClass):
    pass

class SubclassC(SubclassB):
    pass

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from elohim import __version__

setup(
    name='elohim',
    version=__version__,
    packages=find_packages(),
    test_suite="nose.collector",
    tests_require=['nose', 'coverage'],
    extras_require={
        'isora' : ['pyparsing'],
        },
    )

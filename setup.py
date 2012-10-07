#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from elohim import __version__

setup(
    name='elohim',
    description='',
    long_description=open('README').read(),
    author='Wezegege',
    author_email='wezegege@live.fr',
    classifiers=list(),
    keywords=list(),
    version=__version__,
    packages=find_packages(),
    test_suite="nose.collector",
    tests_require=['nose', 'coverage', 'mock'],
    extras_require={
        'isora' : ['pyparsing'],
        },
    )

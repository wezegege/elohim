#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from elohim import __version__

setup(
    name='elohim',
    version=__version__,
    description='',
    author='',
    author_email='',
    packages=find_packages(),
    extra_require={
        'isora' : ['pyparsing'],
        },
    )

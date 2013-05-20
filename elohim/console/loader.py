#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.utils import console

from elohim import loader

@console.command()
def load():
    """Launch a single game
    """
    loader.run()

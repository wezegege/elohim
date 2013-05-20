#!/usr/bin/env python
# -*- coding: utf-8 -*-


from elohim.utils import console

import sys
import shlex


@console.command()
def interactive():
    parser = console.get_command_parser()
    while True:
        user_input = input('>>> ')
        args = shlex.split(user_input)
        console.parse_args(parser, args)


@console.command()
def quit():
    sys.exit(0)


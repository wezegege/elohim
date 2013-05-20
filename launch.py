#!/usr/bin/env python
# -*- coding: utf-8 -*-


import elohim.console
from elohim.utils import console as console_utils

if __name__ == '__main__':
    parser = console_utils.get_command_parser()
    console_utils.parse_args(parser)


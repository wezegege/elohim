#!/usr/bin/env python
# -*- coding: utf-8 -*-


import elohim
import elohim.console

from elohim.utils import console as console_utils

if __name__ == '__main__':
    parser = console_utils.get_command_parser()
    parser.add_argument('-V', '--version', action='version', version='%(prog)s {}'.format(elohim.__version__))

    console_utils.parse_args(parser)


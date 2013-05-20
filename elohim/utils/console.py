#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse

COMMANDS = dict()


def command(parameters=None):
    if parameters is None:
        parameters = list()
    def wrapper(func):
        COMMANDS[func.__name__] = {
            'name' : func.__name__,
            'help' : func.__doc__,
            'parameters' : parameters,
            'func' : func,
            }
        return func
    return wrapper


def get_command_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command",
            title='commands')

    for command in COMMANDS.values():
        subparser = subparsers.add_parser(command['name'],
                help=command['help'])
        for parameter in command['parameters']:
            subparser.add_argument(**parameter)
    return parser

def parse_args(parser, *args, **kwargs):
    result = vars(parser.parse_args(*args, **kwargs))
    prog = result.pop('command')
    COMMANDS[prog]['func'](**result)

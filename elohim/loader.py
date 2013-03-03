#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.client.bot import pig
from elohim.client.ui.console import basic_console

from elohim import settings
from elohim.engine import json_loader, server

import sys
import logging, logging.config
try:
    from six.moves import input
except ImportError:
    pass

logging.config.dictConfig(settings.LOGGING)


def run():
    rules = json_loader.json_files(settings.DATAPATH)
    if not rules:
        print('No game found')
        sys.exit(0)
    elif len(rules) == 1:
        filepath = rules[0]
    else:
        for index, filename in enumerate(rules):
            print('{index:>3} : {filename}'.format(index=index + 1,
                filename=filename))

        max_choice = len(rules)
        while True:
            choice = input('Your choice (1-{max_choice}) : '.format(
                max_choice=max_choice))
            try:
                choice = int(choice)
            except ValueError:
                continue
            if 0 < choice <= max_choice:
                break

        filepath = rules[choice - 1]

    engine = server.Server.from_dict(json_loader.from_json(filepath))
    engine.add_player('Player', basic_console.ConsolePlayer(name='Player'))
    engine.add_player('Bot', pig.PigBot(name='Bot'))

    replay = True
    try:
        while replay:
            engine.play()
            will_replay = input('Wanna play again ? (y/n) ')
            replay = bool(will_replay in ('y', 'yes', 'Y'))
    except (KeyboardInterrupt, EOFError):
        print('Game stopped by user')

if __name__ == '__main__':
    run()

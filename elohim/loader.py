#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.bot import pig
from elohim.client import basic_console

from elohim import settings
from elohim.engine import json_loader, server

import os, os.path, sys

rules = json_loader.json_files(settings.DATAPATH)
if not rules:
    print('No game found')
    sys.exit(0)
elif len(rules) == 1:
    filepath = rules[0]
else:
    for index, filename in enumerate(rules):
        print('{index:>3} : {filename}'.format(index=index + 1, filename=filename))

    max_choice = len(rules)
    while True:
        choice = input('Your choice (1-{max_choice}) : '.format(max_choice=max_choice))
        try:
            choice = int(choice)
        except ValueError:
            continue
        if 0 < choice <= max_choice:
            break

    filepath = rules[choice - 1]

server = server.Server.from_dict(json_loader.from_json(filepath))
server.add_player('Player', basic_console.ConsolePlayer())
server.add_player('Bot', pig.PigBot())

try:
    server.play()
except (KeyboardInterrupt, EOFError):
    print('Game stopped by user')

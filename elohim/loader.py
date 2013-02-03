#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.bot.pig import RandomBot, TurnTotalBot, PigBot
from elohim.client.basic_console import ConsolePlayer

from elohim.engine.json_loader import from_json

import os, os.path

filepath = os.path.join(
    os.getcwd(),
    'data',
    'games',
    'dices',
    'pig',
    'pig.json'
    )
server = from_json(filepath)
server.add_player('Player', ConsolePlayer())
server.add_player('Bot', PigBot())
server.play()

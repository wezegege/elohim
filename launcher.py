#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.bot.pig import RandomBot, TurnTotalBot, PigBot
from elohim.client.basic_console import ConsolePlayer

from elohim.engine.server import Server

import os.path

filepath = os.path.join(
    os.path.dirname(__file__),
    'data',
    'games',
    'dices',
    'pig',
    'pig.json'
    )
server = Server.from_json(filepath)
server.add_player('Player', ConsolePlayer())
server.add_player('Bot', PigBot())
server.play()

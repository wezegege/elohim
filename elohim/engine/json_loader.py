#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.engine.server import Server

import json

def to_json(server, filename):
    content = json.dumps(server.to_dict(), sort_keys=True, indent=4)
    with open(filename, 'w') as f:
        f.write(content)

def from_json(filename):
    with open(filename, 'r') as content:
        gamedata = json.load(content)
    return Server.from_dict(gamedata)


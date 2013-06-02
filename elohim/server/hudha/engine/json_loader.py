#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Import and export games from/to a json format file
"""

import json
import os
import fnmatch

def json_files(rootpath):
    """List json files contained in a given `rootpath`
    """
    result = list()
    for root, _, filenames in os.walk(rootpath):
        goodfiles = fnmatch.filter(filenames, '*.json')
        result.extend(os.path.join(root, f) for f in goodfiles)
    return result

def to_json(gamedata, filename):
    """Transform game data given by a server and save it to a file
    """
    content = json.dumps(gamedata, sort_keys=True, indent=4)
    with open(filename, 'w') as save:
        save.write(content)

def from_json(filename):
    """Open a json file and create a server given its content
    """
    with open(filename, 'r') as content:
        gamedata = json.load(content)
    return gamedata


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import fnmatch

def json_files(rootpath):
    result = list()
    for root, dirnames, filenames in os.walk(rootpath):
        goodfiles = fnmatch.filter(filenames, '*.json')
        result.extend(os.path.join(root, f) for f in goodfiles)
    return result

def to_json(gamedata, filename):
    content = json.dumps(gamedata, sort_keys=True, indent=4)
    with open(filename, 'w') as f:
        f.write(content)

def from_json(filename):
    with open(filename, 'r') as content:
        gamedata = json.load(content)
    return gamedata


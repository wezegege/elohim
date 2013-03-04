#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bot client for turn-based rule engine game
"""

from elohim import client

class Bot(client.Client):
    """Base class for a bot client
    """
    type = 'bot'
    name = 'bot'

    def send(self, message, **kwargs):
        """Receive information from server. Basic operation is to do nothing
        """
        pass


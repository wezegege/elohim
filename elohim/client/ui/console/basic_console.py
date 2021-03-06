#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Pure console client
"""

from elohim.client import ui

try:
    from six.moves import input
except ImportError:
    pass


class ConsolePlayer(ui.Ui):
    """Client for a basic console ui. Require no library
    """
    name = 'console-player'
    library = 'console'

    def send(self, message, **kwargs):
        """Receive a message from the server for treating
        """
        if message == 'playerturn':
            self.display_all([(['score', 'permanent'], 'Score')])
            print("It is {name}'s turn".format(
                name=self.data.get(['players', 'current', 'name'])))
        elif message == 'round':
            self.display_current([
                    (['score', 'permanent'], 'Score'),
                    (['score', 'temporary'], 'Turn total'),
                    ])
        elif message == 'winner':
            self.display_all([(['score', 'permanent'], 'Score')])
            print('{name} wins'.format(name=kwargs['name']))
        elif message == 'choice':
            print('{name} chose to {choice}'.format(
                name=self.data.get(['players', 'current', 'name']),
                choice=kwargs['choice']
                ))
        elif message == 'roll':
            print('{name} rolled a {roll}'.format(
                name=self.data.get(['players', 'current', 'name']),
                roll=kwargs['roll']))

    def askplayer(self, options):
        """Receive a question from the server, which require an answer
        """
        print('Options :')
        width = max(len(field) for field in options.keys())
        for field, value in options.items():
            print('  {field:<{width}} : {value}'.format(
                field=field, width=width, value=value))
        while True:
            result = input('Your choice ({choices}) : '.format(
                choices='|'.join(options.keys())))
            if result in options.keys():
                return result

    def display_all(self, todisplay):
        """Display given fields in data tree of all players
        """
        for player in self.data.get(['players', 'list']):
            print('{name} :'.format(name=player.get(['name'])))
            self.display_one(player, todisplay, 1)

    def display_current(self, todisplay):
        """Display given fields in data tree of the current player
        """
        self.display_one(self.data.get(['players', 'current']), todisplay)

    def display_one(self, player, todisplay, indent=0):
        """Display given fields in data tree of given player
        """
        indent = '  ' * indent
        size = max(len(message) for _, message in todisplay)
        for field, message in todisplay:
            print('{indent}{message:<{width}} : {value}'.format(
                    indent=indent,
                    message=message,
                    width=size,
                    value=player.get(field)))

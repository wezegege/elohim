#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.engine import data


class ConsolePlayer(object):
    def send(self, message, **kwargs):
        if message == 'playerturn':
            self.display_all([(['score', 'permanent'], 'Score')])
            print("It is {name}'s turn".format(name=data.Data.get(['players', 'current', 'name'])))
        elif message == 'round':
            self.display_current([
                    (['score', 'permanent'], 'Score'),
                    (['score', 'temporary'], 'Turn total'),
                    ])
        elif message == 'askcurrent':
            self.askplayer(kwargs['destination'], kwargs['options'])
        elif message == 'winner':
            self.display_all([(['score', 'permanent'], 'Score')])
            print('{name} wins'.format(name=kwargs['name']))
        elif message == 'roll':
            print('You rolled a {roll}'.format(roll=kwargs['roll']))

    def askplayer(self, destination, options):
        print('Options :')
        width = max(len(field) for field in options.keys())
        for field, value in options.items():
            print('  {field:<{width}} : {value}'.format(field=field, width=width, value=value))
        while True:
            result = input('Your choice ({choices}) : '.format(choices='|'.join(options.keys())))
            if result in options.keys():
                data.Data.set(['players', 'current'] + destination, result)
                return

    def display_all(self, todisplay):
        for player in data.Data.get(['players', 'list']):
            print('{name} :'.format(name=player['name']))
            self.display_one(player, todisplay, 1)

    def display_current(self, todisplay):
        self.display_one(data.Data.get(['players', 'current']), todisplay)

    def display_one(self, player, todisplay, indent=0):
        indent = '  ' * indent
        size = max(len(message) for _, message in todisplay)
        for field, message in todisplay:
            print('{indent}{message:<{width}} : {value}'.format(
                    indent=indent,
                    message=message,
                    width=size,
                    value=data.Data.get(field, player)))

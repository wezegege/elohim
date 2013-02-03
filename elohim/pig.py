#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elohim.bot.pig import RandomBot, TurnTotalBot, PigBot
from elohim.client.basic_console import ConsolePlayer

from elohim.action.core import SetWinner, If, ForeachWhile, Sequence
from elohim.action.data import TransferCurrent, SetCurrent, WhileCurrentTrue
from elohim.action.input import AskPlayer
from elohim.action.random import RollDiceCurrent
from elohim.action.pig import AboveCondition, MoveCondition, DiceCondition, PlayerCondition

from elohim.engine.server import Server


game = Sequence(actions = [
    ForeachWhile(condition=PlayerCondition(),
            actions=[
        WhileCurrentTrue(variable=['turn'],
                actions=[
            AskPlayer(destination=['move'],
                options={'hold' : 'Hold points', 'roll' : 'Roll a dice',}),
            If(condition=MoveCondition(),
                iftrue=[
                    RollDiceCurrent(destination=['roll', 'dice'], size=6),
                    If(condition=DiceCondition(),
                        iftrue=[
                            SetCurrent(variable=['score', 'temporary'], value=0),
                            SetCurrent(variable=['turn'], value=False),
                            ],
                        iffalse=[
                            TransferCurrent(origin=['roll', 'dice'],
                                destination=['score', 'temporary'],
                                reset=0),
                            If(condition=AboveCondition(),
                                iftrue=[
                                    TransferCurrent(origin=['score', 'temporary'],
                                        destination=['score', 'permanent'],
                                        reset=0),
                                    SetCurrent(variable=['turn'], value=False),
                                    ],
                                ),
                            ],
                        ),
                    ],
                iffalse=[
                    TransferCurrent(origin=['score', 'temporary'],
                        destination=['score', 'permanent'],
                        reset=0),
                    SetCurrent(variable=['turn'], value=False),
                    ],
                ),
            ],
                ),
        ],
            ),
    SetWinner(criteria=['score', 'permanent']),
    ]
    )


server = Server(game)
server.add_player('Player', ConsolePlayer())
server.add_player('Bot', PigBot())
server.play()

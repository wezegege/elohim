#!/usr/bin/env python
# -*- coding: utf-8 -*-

@describe("The game is called {name}", (
  ('name', 'string'),
  ))
def name(name):
  pass

@describe("It is for {max_players} players at most", (
  ('max_players', 'int'),
  ))
@describe("It is for {min_players} players at least", (
  ('min_players', 'int'),
  ))
@describe("It is for {min_players} to {max_players} players", (
  ('min_players', 'int'),
  ('min_players', 'int'),
  ))
def players(min_players=1, max_players=99):
  pass

@describe("This game is in categories {categories}", (
  ('categories', 'string-list'),
  ))
def categories(categories):
  pass

@describe("Rules are :")
@block('rules')
def rules(rules):
  pass

@describe("For each player until {source} {comparision} {destination}", (
  ('source', 'variable'),
  ('comparison', 'operator'),
  ('destination', 'variable'),
  ))
@describe("For each player until {source} {comparision} {value}", (
  ('source', 'variable'),
  ('comparison', 'operator'),
  ('value', 'int-or-string'),
  ))
@block('actions')
def foreach_compare(source, comparison, actions, destination=None, value=None):
  pass

@describe("While player's turn continue")
@block('actions')
def continue(actions):
  pass

@describe("Face player with these options")
@block("- option \d+ :", 'options')
def options(options):
  pass

@describe("Tranfer {source} to {destination}", (
  ('source', 'variable'),
  ('destination', 'variable'),
  ))
def transfer(source, destination):
  pass

@describe("End turn")
def end_turn():
  pass

@describe("Roll a d{size}", (
  ('size', 'int'),
  ))
@describe("Roll a dice")
def roll_dice(size=6):
  pass

@describe("If {source} {comparison} {destination}", (
  ('source', 'variable'),
  ('comparison', 'operator'),
  ('destination', 'variable'),
  ))
@describe("If {source} {comparision} {value}", (
  ('source', 'variable'),
  ('comparison', 'operator'),
  ('value', 'int-or-string'),
  ))
@block("Then", 'true_branch')
@block("Else", 'false_branch')
def test(source, comparison, true_branch, false_branch, destination=None, value=None):
  pass

@describe("Reset {variable}", (
  ('variable', 'variable'),
  ))
def reset(variable):
  pass

@describe("Add {source} to {destination}", (
  ('source', 'variable'),
  ('destination', 'variable'),
  ))
@describe("Add {value} to {destination}", (
  ('value', 'int'),
  ('destination', 'variable'),
  ))
def add_variable(destination, source=None, value=None):
  pass

@describe("Winner is the one with the {min_max} {score}", (
  ('min_max', 'enum', ('best', 'worst')),
  ('score', 'variable'),
  ))
def winner_compare(min_max, score):
  pass

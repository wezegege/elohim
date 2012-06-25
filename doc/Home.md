=============
PokerTemplate
=============

* * *

------------
Introduction
------------

This project is about an engine allowing users to create a game with simple language, and to share and play it online or against bots.

The original aim of this project was to play a poker variant and try some various AI, but I also wanted to implement some other variants. As most of poker variants a same baseline, I imagined a simple language to describe most of poker variants rules. As time goes by, poker games scope became cards games, then all kind of games.

The language will first permit to describe cards and board games, and will be quite high level. It is designed around libraries, so that the adding of new rules is made simple. The four first libraries will be the core commands, the cards-related functions, the money-related ones, and the pawns-related one. An interface for poker games is scheduled, but there is currently no plan on giving a common interface for cards or board games. At first glance, they can be so different that the resulted interface will be to complicated to configure, but maybe a further thought  on it will prove it wrong.

The application will be able to manage local network games as long as internet games, mixed with some bots. The server-side for an Internet scope is not in the todolist for now, but the application will account for it. For lan mode, either the one who created the game, or the one with best latency will host the server.

Bots will be associated with one or several games. They are also managed with dynamic libraries, so that one can easily create and share its own one. 

* * *

--------
Features
--------

Chatting
========

# Description

Message is sent to player if present, stored to a server otherwise for later reading

# Implementation

## Structure

Message will be stored as a tree structure :

    /wisps
    /chans
    /parties
    /clans
    /games/all
    /games/allies
    /games/spectator
    /topics

## Classes

    client
    ------
    write()
    channel

    chanDirectory
    -------------
    post()
    channel->user

    userDirectory
    -------------
    send()
    user->ip

    serverContainer
    ---------------
    post()
    channel->index

    authenticator
    -------------
    checkUID
    getUID
    uid
    nickname

## Algorithm

When a message is submitted by user :

1. assign user as submitter
2. find server location
3. (if we do not host the server) send to network
4. (else) send to server

When a message is submitted from network :

1. check server location
2. (if wrong location) send back to sender
3. (else) send to server

When a channel server receive a message :

1. check whether sender has permission to post (voice, ...)
2. check whether sender is flooding
3. send message with list of all channel users

When a whisp server receive a message :

1. send to user a message with sender's name replacing our in channel name
2. send back a message to sender

When a message is published by a server :

1. send to network-wide followers
2. check for preferences (ignores, ...)
3. log message
4. send to suscribers

# References

* [IRC protocol](http://en.wikipedia.org/wiki/Internet_Relay_Chat)

* * *

Social
======

# Features

* Friend list
* Recently encountered people
* Team (may have several)

------
Topics
------

# Network

# Interface

# Engine

# Artificial intelligence

# Data storage

-----------
Development
-----------

# Tools

# Logging

# Profile

# Localization

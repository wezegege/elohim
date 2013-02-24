#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

ROOTPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATAPATH = os.path.join(ROOTPATH, 'resources')

LOGGING = {
    'version' : 1,
    'disable_existing_loggers' : True,
    'formatters' : {
      'verbose' : {
        'format' : '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
      'simple': {
        'format': '%(levelname)s %(message)s',
        },
      },
    'handlers': {
      'console':{
        'level':'DEBUG',
        'class':'logging.StreamHandler',
        'formatter': 'simple',
        },
      'file' : {
        'level':'DEBUG',
        'class':'logging.FileHandler',
        'formatter':'verbose',
        'filename':os.path.join(ROOTPATH, 'elohim.log')

        }
      },
    'loggers': {
      'elohim': {
        'handlers':['console','file'],
        'propagate':True,
        'level':'INFO',
        }
      }
    }

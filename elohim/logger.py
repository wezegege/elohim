#!/usr/bin/env python
# -*- coding: utf-8 -*-


from elohim import settings

import multiprocessing
import logging
from logging import handlers

import os
from os import path


class LoggerFabric(object):
    logs = dict()

    config_file = 'logs.cfg'
    file_size = 1024 * 1024
    backup_count = 7

    @classmethod
    def get_logger(cls, name, prefix=''):
        if name in cls.logs:
            return cls.logs[name]
        logger = logging.getLogger(prefix + name)
        logger.propagate = False
        logger.setLevel(logging.DEBUG)

        log_file = path.join(settings.LOG_PATH, *name.split('.')) + '.log'
        log_dir = path.dirname(log_file)
        if not path.exists(log_dir):
            os.makedirs(log_dir)
        fileHandler = handlers.RotatingFileHandler(log_file,
                maxBytes=cls.file_size,
                backupCount=cls.backup_count)
        logger.addHandler(fileHandler)

        self.logs[name] = logger
        return logger


class LoggerProcess(multiprocessing.Process):

    def __init__(self, loophandler=None, message_queue=None):
        super(LoggerProcess, self).__init__(name='Logger')
        self.message_queue = multiprocessing.Queue() \
                if message_queue is None else message_queue
        self.initialize()
        self.logger = logging.getLogger(__name__)
        self.logger.debug('Finished logger initialization')
        self.loophandler = loophandlers.LoopHandler() \
                if loophandler is None else loophandler

    def createHandler(self):
        class QueueHandler(logging.Handler):
            def __init__(queue, *args, **kwargs):
                super(QueueHandler, queue).__init__(*args, **kwargs)
                queue.message_queue = self.message_queue

            def emit(queue, record):
                if __name__ != record.name:
                    log = logging.getLogger(__name__)
                    log.debug('Treating log for {} : {}'.format(record.name, record.msg))
                queue.message_queue.put(record)

        return QueueHandler()

    def initialize(self):
        serverLogger = logging.getLogger('log')
        serverLogger.propagate = False
        serverLogger.setLevel(logging.DEBUG)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)
        serverLogger.addHandler(consoleHandler)

        clientLogger = logging.getLogger()
        clientLogger.setLevel(logging.DEBUG)

        queueHandler = self.createHandler()
        queueHandler.setLevel(logging.DEBUG)
        clientLogger.addHandler(queueHandler)
        clientLogger.addHandler(consoleHandler)

    def queue_size(self):
        return self.message_queue.qsize()

    def run(self):
        self.logger.debug('Starting logger process')
        while True:
            record = self.message_queue.get()
            with self.loophandler:
                if not isinstance(record, logging.LogRecord):
                    break
                logger = LoggerFabric.get_logger(record.name, prefix='log.')
                logger.handle(record)
        LoggerFabric.get_logger(__name__).debug('Ending logger process')

    def end(self):
        self.logger.debug('Sending stop message')
        self.message_queue.put(None)


if __name__ == '__main__':
    logger = LoggerProcess()
    logger.start()
    log = logging.getLogger()
    log.info('test')
    logger.end()
    logger.join()


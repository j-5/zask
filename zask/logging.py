# -*- coding: utf-8 -*-
"""
    zask.logging
    ~~~~~~~~~~~~~

    Implements the logging support for Zask.

    :copyright: (c) 2015 by the J5.
    :license: BSD, see LICENSE for more details.
"""

from __future__ import absolute_import

from logging.handlers import RotatingFileHandler
import logging
import logging.config


PROD_LOG_FORMAT = (
    '[%(asctime)s] ' +
    '%(name)s %(levelname)s in %(module)s ' +
    '[%(pathname)s:%(lineno)d]: %(message)s'
)
DEBUG_LOG_FORMAT = (
    '-' * 40 + '\n' +
    '%(name)s %(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n' +
    '%(message)s\n'
)


def debug_handler():
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(DEBUG_LOG_FORMAT))
    return handler


def production_handler(config):
    handler = RotatingFileHandler(config['ERROR_LOG'],
                                  maxBytes=1024 * 50,
                                  backupCount=5)
    handler.setLevel(_get_production_logging_level(config))
    handler.setFormatter(logging.Formatter(PROD_LOG_FORMAT))
    return handler


def create_logger(config):
    """Creates a logger for the application. Logger's behavior depend on
    ``DEBUG`` flag.Furthermore this function also removes all attached
    handlers in case there was a logger with the log name before.
    if there is LOGGING section in config use the dictConfig to create
    logger for production or debug.
    """
    logging_config = config.get('LOGGING')
    if logging_config is not None:
        logging.config.dictConfig(logging_config)
        if config['DEBUG']:
            logger_ = logging.getLogger('zask.debug')
        else:
            logger_ = logging.getLogger('zask.production')
    else:
        logger_ = logging.getLogger(__name__)
        del logger_.handlers[:]

        if config['DEBUG']:
            handler = debug_handler()
            logger_.setLevel(logging.DEBUG)
        else:
            handler = production_handler(config)
            logger_.setLevel(_get_production_logging_level(config))

        logger_.addHandler(handler)
    return logger_


def _get_production_logging_level(config):
    config.setdefault('PRODUCTION_LOGGING_LEVEL', 'INFO')
    mapping = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR
    }
    return mapping.get(config['PRODUCTION_LOGGING_LEVEL'].upper())\
           or logging.INFO

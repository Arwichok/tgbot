import logging
from logging import DEBUG, INFO

from . import config


def setup_log():
    logging.basicConfig(
        level=[INFO, DEBUG][config.DEBUG],
        format=config.LOG_FORMAT,
        datefmt="%Y-%m-%d %H:%M:%S %z")

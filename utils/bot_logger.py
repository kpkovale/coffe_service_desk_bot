# Core telebot modules
import logging

from telebot import logger

# logging level
from config import LOG_LEVEL, BASE_DIR
from logging import FileHandler, Formatter
from logging.handlers import RotatingFileHandler
import sys
import os


# set logger
logger = logger
logger.setLevel(LOG_LEVEL)

log_path = str(BASE_DIR) + '/logs/app.log'
if not os.path.exists(log_path):
    open(log_path, "a").close()

full_formatter = Formatter(
    '%(levelname)s %(asctime)s (%(filename)-20s:%(lineno)-4d %(threadName)s) - %(name)s: "%(message)s"'
)
console_formatter = Formatter(
    '%(levelname)s %(asctime)s (%(threadName)s %(filename)-20s:%(lineno)-4d) - %(name)s: "%(message)s"',
    datefmt="%Y-%m-%d %H:%M:%S"
)
# set file handler
err_file_handler = RotatingFileHandler(log_path, maxBytes=1024*1024, backupCount=4, encoding='utf-8')
err_file_handler.setFormatter(full_formatter)
err_file_handler.setLevel(logging.ERROR)

# set logger
logger = logger
logger.setLevel(LOG_LEVEL)
logger.addHandler(err_file_handler)

logger.handlers[0].setFormatter(console_formatter)

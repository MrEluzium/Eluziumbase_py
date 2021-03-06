import logging
import sys


FORMATTER = logging.Formatter(
        fmt="[%(asctime)s] [%(filename)s:%(lineno)d] %(levelname)s: %(message)s",
        datefmt="%d/%b/%Y %H:%M:%S")
LOG_FILE = "here.log"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger

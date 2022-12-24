r'''
File that describe logger for  Telegram chat bot.

Author: 2022 Nikita Kulikov
'''

import logging
import logging.handlers
from pathlib import Path
_log_format = f"%(asctime)s : [%(levelname)s] - %(name)s - (%(filename)s.%(funcName)s(%(lineno)d) - %(message)s"


def get_file_handler(id: int) -> logging.Handler:
    r'''
    Getting File Handler for logger
    '''
    file_handler = logging.FileHandler(Path('logs/%s.log' % id), encoding='utf-8')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler() -> logging.Handler:
    r'''
    Getting Stream Handler for logger
    '''
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def get_rotation_handler() -> logging.Handler:
    r'''
    Getting Rotating File Handler for logger
    '''
    rotation_handler = logging.handlers.RotatingFileHandler(
        filename=Path('logs/logging.log'),
        maxBytes=1000000,
        backupCount=6,
        encoding='utf-8'
    )
    return rotation_handler


def get_logger(name=__name__) -> logging.Logger:
    r'''
    Get logger object with:
    level = INFO,
    File Handler,
    Stream Handler,
    Rotation Handler (1MB size, 2 files per user)
    '''
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_rotation_handler())
    logger.addHandler(get_stream_handler())
    return logger

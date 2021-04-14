""" A basic logger to handle all the execution messages"""
import logging
import os
import datetime
import sys
from functools import lru_cache


class LogSystem(object):
    """ Generates a new logger """
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not LogSystem.__instance:
            LogSystem.__instance = object.__new__(cls)
        return LogSystem.__instance

    @lru_cache(maxsize=16)
    def __init__(self, log_dir='./logs', name=None, log_name=None):
        self.name = datetime.datetime.now().strftime('logfile_%H_%M_%d_%m_%Y.log') if not name else name
        self.name = "/".join((log_dir, self.name))
        self.log_name = 'logfile' if not log_name else log_name
        self.log_dir = log_dir
        self.logging = None

        self._create_dir(self.log_dir)
        self._initialize_logger()

    @staticmethod
    def _create_dir(log_dir):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def _initialize_logger(self):
        logger = logging.getLogger(self.log_name)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        logger.propagate = False

        file_handler = logging.FileHandler(self.name, mode='a')
        file_handler.setFormatter(formatter)

        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        self.logging = logger

    def log_info(self, message):
        try:
            self.logging.info(message)
        except Exception as e:
            print(f'Error when trying to log file {str(self.name)} {str(e)}')

    def log_error(self, message):
        try:
            self.logging.error(message)
        except Exception as e:
            print(f'Error when trying to log file {str(self.name)} {str(e)}')
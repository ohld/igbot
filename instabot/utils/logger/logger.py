import logging
import os
from logging.handlers import TimedRotatingFileHandler

from instabot.utils.generic_utils.singleton import Singleton


class Logger(metaclass=Singleton):
    CONSOLE_FORMAT = logging.Formatter("%(asctime)s - %(levelname)s - [%(logger_id)s]: %(message)s")
    FILE_FORMAT = logging.Formatter("%(asctime)s - %(levelname)s - [%(logger_id)s]: %(message)s")

    def __init__(self):
        self.loggers = dict()

    def __create_logger__(self, logger_id, log_path=None, save_logfile=True, log_filename=None):
        self.loggers[logger_id] = logging.getLogger(logger_id)
        self.loggers[logger_id].setLevel(logging.DEBUG)

        if save_logfile is True:
            self.log_path = log_path + 'logs'
            if self.log_path is None:
                self.log_path = 'logs'
            if log_filename is None:
                if not os.path.exists(self.log_path):
                    os.makedirs(self.log_path)
                self.log_filename = os.path.join(self.log_path, "instabot_.log")
            self.__add_file_rotating_handler__(logger_id=logger_id)

        self.__add_console_stream_handler__(logger_id=logger_id)
        return self.loggers[logger_id]

    def __add_file_rotating_handler__(self, logger_id, level=logging.INFO):
        fh = TimedRotatingFileHandler(filename=self.log_filename, when='midnight', backupCount=50)
        fh.setLevel(level)
        fh.setFormatter(self.FILE_FORMAT)
        self.loggers[logger_id].addHandler(fh)

    def __add_console_stream_handler__(self, logger_id, level=logging.DEBUG):
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(self.CONSOLE_FORMAT)
        self.loggers[logger_id].addHandler(ch)

    def __add_logger_id_adapter__(self, logger_id):
        extra = {'logger_id': logger_id}
        self.loggers[logger_id] = logging.LoggerAdapter(self.loggers[logger_id], extra)

    def get_logger(self, logger_id, log_path=None, save_logfile=True, log_filename=None):
        try:
            return self.loggers[logger_id]
        except KeyError:
            return self.__create_logger__(logger_id, log_path, save_logfile, log_filename)

import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler
from logging import StreamHandler
from enum import Enum

class LogType(Enum):
    FILE    = 1
    CONSOLE = 2
    
class Log:
    _LOGGER = None
    
    @staticmethod
    def create(logType, dir, name, level):
        Log._LOGGER = logging.getLogger()
        Log._LOGGER.setLevel(level)
        
        fileFormat  = "[%(levelname)s|%(name)s|%(threadName)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s"
        
        if logType == LogType.FILE:
            handler = RotatingFileHandler(f"{dir}{name}".format(dir), maxBytes = 1024 * 1024, backupCount = 10)
        else:
            handler = StreamHandler()
        
        handler.setLevel(level)
        handler.setFormatter(Formatter(fileFormat))
        
        Log._LOGGER.addHandler(handler)
    
    @classmethod
    def log(cls):
        return cls._LOGGER

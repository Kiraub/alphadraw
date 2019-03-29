from enum import Enum
from xexcerr import IllegalCharacterException

class LogLevel(Enum):
    VERBOSE = 0
    DEBUG = 1
    INFO = 3
    EXC = 5
    ERR = 7
    MSG = 10

class Logger():
    def __init__(self, level=LogLevel.EXC):
        self.__level = level
    def level(self, val=None):
        if val is None:
            return self.__level
        elif val in LogLevel:
            self.__level = val
        elif val in range(0,11):
            self.__level = LogLevel(val)
        else:
            raise IllegalCharacterException("Illegal log level '"+str(val)+"'.", None)
    def log(self, level, *msg, sep="\n", indent=0):
        if level.value >= self.level().value:
            for m in msg:
                print( LogLevel(level.value).name[0:3] + ".>" + " "*indent, str(m), end=sep)
        else:
            # Omitted message due to log level
            pass
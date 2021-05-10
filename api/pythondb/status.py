from enum import Enum

@unique
class Status(Enum):
    OK = 'OK'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
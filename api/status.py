from enum import Enum, unique

@unique
class Status(Enum):
    OK = 'OK'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
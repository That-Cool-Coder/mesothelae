class FileCorrupted(Exception):
    pass

class NoDatabaseProvided(Exception):
    pass

class NoRowProvided(Exception):
    pass

class InvalidFieldPath(Exception):
    pass

class FieldDuplicated(Exception):
    pass

# Not actually used
class DatabaseObjectCorrupted(Exception):
    pass
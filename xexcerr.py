
class IllegalCharacterException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors

class NoDefinitionException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors
class CommandSyntaxError(Exception):
    """Raised when a command has invalid syntax."""

    def __init__(self, message="ERR Syntax error"):
        super().__init__(message)


class WrongNumberOfArgsError(Exception):
    """Raised when a command has wrong number of args."""

    def __init__(self, message="ERR Wrong number of arguments for the command"):
        super().__init__(message)

from .meta import CommandMeta


class BaseCommand(metaclass=CommandMeta):
    """
    A base class for commands using the CommandMeta metaclass.
    """

    name = None  # Command name, to be defined in subclasses

    def __init__(self, description=""):
        self.description = description

    def validate_args(self, *args, **kwargs):
        """
        Validates the args for a command
        """
        raise NotImplementedError("Subclasses must implement the `validate_args` method.")

    def execute(self, *args, **kwargs):
        """
        Execute the command. Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the `execute` method.")

    def __call__(self, *args, **kwargs):
        """
        Call the command like a function.
        """
        return self.execute(*args, **kwargs)

    def help(self):
        """
        Display help information about the command.
        """
        return f"Command: {self.name}\nDescription: {self.description}"

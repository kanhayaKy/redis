class CommandMeta(type):
    """
    A metaclass that automatically registers commands by name.
    """

    registry = {}

    def __new__(cls, name, bases, dct):
        # Create the new class
        command_class = super().__new__(cls, name, bases, dct)

        # Register the class if it has a 'name' attribute
        if hasattr(command_class, "name") and command_class.name:
            if command_class.name in cls.registry:
                raise ValueError(
                    f"Command '{command_class.name}' is already registered."
                )
            cls.registry[command_class.name] = command_class

        return command_class

    @classmethod
    def get_command(cls, name):
        """
        Retrieve a command class by name.
        """
        return cls.registry.get(name.upper())

    @classmethod
    def get_command_callable(cls, name):
        """
        Retrieve a command instance by name.
        """

        if name.upper() not in cls.registry:
            raise Exception(
                f"Invalid Command, valid commands are {CommandMeta.list_commands()}"
            )
        command = CommandMeta.get_command(name)
        return command()

    @classmethod
    def list_commands(cls):
        """
        List all registered command names.
        """
        return list(cls.registry.keys())

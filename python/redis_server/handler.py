from utils import RESPSerializer, RESPParser

from commands import CommandMeta


def process_request(request):
    parsed_request = RESPParser(request).parse()

    command_name = parsed_request[0]

    command = CommandMeta.get_command_callable(command_name)

    if not command:
        return RESPSerializer("ERR Invalid command").serialize(error=True)

    command_args = parsed_request[1:]

    # Validate args
    command.validate_args(*command_args)
    response = command(*command_args)

    return RESPSerializer(response).serialize()

from .base import BaseCommand
from redis_server.exceptions import WrongNumberOfArgsError


class EchoCommand(BaseCommand):
    name = "ECHO"

    def __init__(self):
        super().__init__(description="Returns the arguments back.")

    def validate_args(self, *args):
        if len(args) != 1:
            raise WrongNumberOfArgsError

    def execute(self, args):
        return args

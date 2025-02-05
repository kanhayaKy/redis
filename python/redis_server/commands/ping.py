from redis_server.exceptions import WrongNumberOfArgsError
from .base import BaseCommand


class PingCommand(BaseCommand):
    name = "PING"

    def __init__(self):
        super().__init__(description="Responds with 'PONG'.")

    def validate_args(self, *args):
        super().validate_args(*args)

        if len(args) > 0:
            raise WrongNumberOfArgsError

    def execute(self):
        return "PONG"

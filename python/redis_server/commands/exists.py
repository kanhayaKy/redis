from .base import BaseCommand
from .store import RedisStore

from redis_server.exceptions import WrongNumberOfArgsError


class ExistsCommand(BaseCommand):
    name = "EXISTS"

    def __init__(self):
        super().__init__(description="Check if values for the given keys exists.")

    def validate_args(self, *args):
        if len(args) != 1:
            raise WrongNumberOfArgsError

    def execute(self, *keys):
        count = 0
        for key in keys:
            if key in RedisStore:
                count += 1

        return count

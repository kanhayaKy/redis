from .base import BaseCommand
from .store import RedisStore

from redis_server.exceptions import WrongNumberOfArgsError


class DelCommand(BaseCommand):
    name = "DEL"

    def __init__(self):
        super().__init__(description="Deletes the given keys.")

    def validate_args(self, *args):
        super().validate_args(*args)

        if len(args) < 1:
            raise WrongNumberOfArgsError

    def execute(self, *keys):
        count = 0
        for key in keys:
            if key in RedisStore:
                RedisStore.delete(key)
                count += 1

        return count

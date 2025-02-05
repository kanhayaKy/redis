from .base import BaseCommand
from .store import RedisStore

from redis_server.exceptions import WrongNumberOfArgsError


class GetCommand(BaseCommand):
    name = "GET"

    def __init__(self):
        super().__init__(description="Returns the value for the given key.")

    def validate_args(self, *args):
        if len(args) != 1:
            raise WrongNumberOfArgsError

    def execute(self, key):
        return RedisStore.get(key)

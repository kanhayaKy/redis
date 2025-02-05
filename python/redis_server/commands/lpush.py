from collections import deque

from redis_server.exceptions import WrongNumberOfArgsError

from .base import BaseCommand
from .store import RedisStore


class LPushCommand(BaseCommand):
    name = "LPUSH"

    def __init__(self):
        super().__init__(
            description="Insert all the specified values at the head of the list stored at key"
        )

    def validate_args(self, *args):
        super().validate_args(*args)

        if len(args) < 2:
            raise WrongNumberOfArgsError

    def execute(self, key, *values):
        if key not in RedisStore:
            RedisStore.set(key, deque([]))

        current_value = deque(RedisStore.get(key))

        for value in values:
            current_value.appendleft(value)

        RedisStore.set(key, current_value)
        return len(current_value)

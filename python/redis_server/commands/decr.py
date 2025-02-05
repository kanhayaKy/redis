from .base import BaseCommand
from .store import RedisStore
from redis_server.exceptions import WrongNumberOfArgsError


class DecrCommand(BaseCommand):
    name = "DECR"

    def __init__(self):
        super().__init__(description="Decrements the given key's value by 1.")

    def validate_args(self, *args):
        super().validate_args(*args)

        if len(args) != 1:
            raise WrongNumberOfArgsError()

    def execute(self, key):
        if key not in RedisStore:
            RedisStore.set(key, 0)

        current = RedisStore.get(key)

        try:
            current_int = int(current)
        except Exception as e:
            raise Exception("WRONGTYPE expected integer value for the key")

        RedisStore.set(key, current_int - 1)

        return RedisStore.get(key)

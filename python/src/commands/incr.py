from .base import BaseCommand
from .store import RedisStore


class IncrCommand(BaseCommand):
    name = "INCR"

    def __init__(self):
        super().__init__(description="Increments the given key's value by 1.")

    def execute(self, key):
        if key not in RedisStore:
            RedisStore.set(key, 0)

        current = RedisStore.get(key)

        try:
            current_int = int(current)
        except Exception as e:
            raise Exception("WRONGTYPE expected integer value for the key")

        RedisStore.set(key, current_int + 1)

        return RedisStore.get(key)

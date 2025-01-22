from .base import BaseCommand
from .store import RedisStore


class DelCommand(BaseCommand):
    name = "DEL"

    def __init__(self):
        super().__init__(description="Deletes the given keys.")

    def execute(self, *keys):
        count = 0
        for key in keys:
            if key in RedisStore:
                RedisStore.delete(key)
                count += 1

        return count

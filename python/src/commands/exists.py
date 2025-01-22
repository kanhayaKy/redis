from .base import BaseCommand
from .store import RedisStore


class ExistsCommand(BaseCommand):
    name = "EXISTS"

    def __init__(self):
        super().__init__(description="Check if values for the given keys exists.")

    def execute(self, *keys):
        count = 0
        for key in keys:
            if key in RedisStore:
                count += 1

        return count

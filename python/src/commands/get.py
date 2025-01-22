from .base import BaseCommand
from .store import RedisStore


class GetCommand(BaseCommand):
    name = "GET"

    def __init__(self):
        super().__init__(description="Returns the value for the given key.")

    def execute(self, key):
        return RedisStore.get(key)

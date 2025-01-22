from .base import BaseCommand
from .store import RedisStore


class SetCommand(BaseCommand):
    name = "SET"

    def __init__(self):
        super().__init__(description="Sets the value for the given key.")

    def execute(self, key, value):
        RedisStore.set(key, value)
        return "OK"

from .base import BaseCommand
from .store import RedisStore


class SaveCommand(BaseCommand):
    name = "SAVE"

    def __init__(self):
        super().__init__(description="Saves the db to the disk.")

    def execute(self):
        RedisStore.save()
        return "OK"

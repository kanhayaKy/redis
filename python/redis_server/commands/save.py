from redis_server.exceptions import WrongNumberOfArgsError
from .base import BaseCommand
from .store import RedisStore


class SaveCommand(BaseCommand):
    name = "SAVE"

    def __init__(self):
        super().__init__(description="Saves the db to the disk.")

    def validate_args(self, *args):
        super().validate_args(*args)

        if len(args) > 0:
            raise WrongNumberOfArgsError

    def execute(self):
        RedisStore.save()
        return "OK"

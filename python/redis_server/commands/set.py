from .base import BaseCommand
from .store import RedisStore
from redis_server.utils import (
    get_expiry_time_unix_ms,
    get_expiry_time_milliseconds,
    get_expiry_time_seconds,
    get_expiry_time_unix,
)

from redis_server.exceptions import CommandSyntaxError, WrongNumberOfArgsError


class SetCommand(BaseCommand):
    name = "SET"
    supported_options = {
        "EX": get_expiry_time_seconds,
        "PX": get_expiry_time_milliseconds,
        "EAXT": get_expiry_time_unix,
        "PXAT": get_expiry_time_unix_ms,
    }

    def __init__(self):
        super().__init__(description="Sets the value for the given key.")

    def validate_args(self, *args):
        super().validate_args(*args)
        if len(args) < 2:
            raise WrongNumberOfArgsError()

    def parse_args(self, args):
        if len(args) > 2:
            raise CommandSyntaxError()

        option_name = args[0]

        if option_name.upper() not in self.supported_options:
            raise CommandSyntaxError()

        if option_name and len(args) < 2:
            raise CommandSyntaxError()

        option_value = args[1]

        return option_name.upper(), int(option_value)

    def execute(self, key, value, *extra_args):
        expiry_value = None

        if extra_args:
            option, expiry = self.parse_args(extra_args)
            expiry_value = self.supported_options[option](expiry)

        RedisStore.set(key, value, expiry_value)
        return "OK"

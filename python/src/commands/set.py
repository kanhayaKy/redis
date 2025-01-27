from .base import BaseCommand
from .store import RedisStore
from utils import (
    get_expiry_time_unix_ms,
    get_expiry_time_milliseconds,
    get_expiry_time_seconds,
    get_expiry_time_unix,
)


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

    def parse_args(self, args):
        if len(args) > 2:
            raise Exception("Syntax error")

        option_name = args[0]

        if option_name.upper() not in self.supported_options:
            raise Exception("Syntax error, invalid option")

        if option_name and len(args) < 2:
            raise Exception("Syntax error, invalid option")

        option_value = args[1]

        return option_name.upper(), int(option_value)

    def execute(self, key, value, *extra_args):
        expiry_value = None

        if extra_args:
            option, expiry = self.parse_args(extra_args)
            expiry_value = self.supported_options[option](expiry)

        RedisStore.set(key, value, expiry_value)
        return "OK"

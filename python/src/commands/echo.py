from .base import BaseCommand


class EchoCommand(BaseCommand):
    name = "ECHO"

    def __init__(self):
        super().__init__(description="Returns the arguments back.")

    def execute(self, *args):
        return args

from .base import BaseCommand


class PingCommand(BaseCommand):
    name = "PING"

    def __init__(self):
        super().__init__(description="Responds with 'PONG'.")

    def execute(self, *args):
        return "PONG"

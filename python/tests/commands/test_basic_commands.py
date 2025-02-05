import pytest

from redis_server.commands import (
    PingCommand,
    EchoCommand,
    ExistsCommand,
    IncrCommand,
    DecrCommand,
    SaveCommand,
)
from redis_server.commands.store import RedisStore


def test_ping_command():
    assert PingCommand()() == "PONG"


@pytest.mark.parametrize("value", ["Hello", "Hello world", "Lorem ipsum foo"])
def test_ping_command(value):
    assert EchoCommand()(value) == value


def test_exists():
    RedisStore.set("foo", "exists")
    assert ExistsCommand()("foo", "bar") == 1


def test_incr():
    RedisStore.set("incr1", 2)

    assert IncrCommand()("incr0") == 1
    assert IncrCommand()("incr1") == 3


def test_decr():
    RedisStore.set("decr1", 2)

    assert DecrCommand()("decr0") == -1
    assert DecrCommand()("decr1") == 1


def test_save():
    assert SaveCommand()() == "OK"

import pytest

from redis_server.commands import (
    PingCommand,
    EchoCommand,
    ExistsCommand,
    IncrCommand,
    DecrCommand,
    SaveCommand,
    LPushCommand,
    RPushCommand,
    DelCommand,
)
from redis_server.commands.store import RedisStore


@pytest.fixture(autouse=True)
def reset_table():
    # This fixture runs automatically before each test
    RedisStore.reset_db()


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


def test_del():
    RedisStore.set("del1", 1)
    RedisStore.set("del2", 2)

    DelCommand()("del1")

    assert RedisStore.get("del1") == None
    assert RedisStore.get("del2") == 2


def test_save():
    assert SaveCommand()() == "OK"


def test_lpush():
    assert LPushCommand()("lpush-key", [1, 2, 3]) == 3

    value = RedisStore.get("lpush-key")
    assert list(value) == [3, 2, 1]


def test_rpush():
    assert RPushCommand()("rpush-key", [1, 2, 3, 4, 5]) == 5

    value = RedisStore.get("rpush-key")
    assert list(value) == [1, 2, 3, 4, 5]

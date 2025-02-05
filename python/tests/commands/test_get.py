import pytest

from redis_server.commands import GetCommand
from redis_server.commands.store import RedisStore


@pytest.mark.parametrize("key,value", [("key1", "value1"), ("key2", "value2")])
def test_get(key, value):
    RedisStore.set(key, value)
    assert GetCommand()(key) == value


def test_non_existent_key():
    assert GetCommand()("non_existent_key") is None

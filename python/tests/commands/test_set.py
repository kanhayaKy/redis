import pytest

from redis_server.commands import SetCommand
from redis_server.commands.store import RedisStore
from redis_server.utils import (
    get_current_ts,
    get_expiry_time_seconds,
    get_expiry_time_milliseconds,
    get_expiry_time_unix_ms,
    get_expiry_time_unix,
)

from redis_server.exceptions import CommandSyntaxError


@pytest.mark.parametrize("key,value", [("key1", "value1"), ("key2", "value2")])
def test_set(key, value):
    SetCommand()(key, value)
    assert RedisStore.get(key) == value


def test_set_invalid_option():
    with pytest.raises(CommandSyntaxError) as exc_info:
        SetCommand()("key", "value", "rx", 3)


def test_set_without_expiry():
    SetCommand()("test-key", "test-value")
    assert RedisStore.get("test-key") == "test-value"
    assert RedisStore.get_expiry("test-key") is None


def test_set_ex_option():
    SetCommand()("ex-key", "ex-value", "ex", 3)
    assert RedisStore.get("ex-key") == "ex-value"
    assert RedisStore.get_expiry("ex-key") == get_expiry_time_seconds(3)


def test_set_px_option():
    SetCommand()("px-key", "px-value", "px", 3000)
    assert RedisStore.get("px-key") == "px-value"
    assert RedisStore.get_expiry("px-key") == get_expiry_time_milliseconds(3000)


def test_set_eaxt_option():
    ts = get_current_ts() + 5 * 60 * 60  # 5 Hours from now

    SetCommand()("eaxt-key", "eaxt-value", "eaxt", ts)

    assert RedisStore.get("eaxt-key") == "eaxt-value"
    assert RedisStore.get_expiry("eaxt-key") == get_expiry_time_unix(ts)


def test_set_paxt_option():
    ts = get_expiry_time_unix_ms(get_current_ts() + 5 * 60 * 60)  # 5 Hours from now

    SetCommand()("pxat-key", "pxat-value", "pxat", ts)

    assert RedisStore.get("pxat-key") == "pxat-value"
    assert RedisStore.get_expiry("pxat-key") == ts

import pytest
from utils import RESPParser, RESPSerializer

happy_cases = [
    (b"$-1\r\n", None, True, False),
    (b"*1\r\n$4\r\nping\r\n", ["ping"], False, False),
    (
        b"*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n",
        ["echo", "hello world"],
        False,
        False,
    ),
    (b"*2\r\n$3\r\nget\r\n$3\r\nkey\r\n", ["get", "key"], False, False),
    (b"+OK\r\n", "OK", False, False),
    (b"-Error message\r\n", "Error message", False, True),
    (b"$0\r\n\r\n", "", True, False),
    (b"+hello world\r\n", "hello world", False, False),
]


@pytest.mark.parametrize("resp, expected, bulk, error", happy_cases)
def test_resp_parsing(resp, expected, bulk, error):
    parser = RESPParser(resp)
    assert parser.parse() == expected


@pytest.mark.parametrize("expected, resp, bulk, error", happy_cases)
def test_resp_serializing(resp, expected, bulk, error):
    parser = RESPSerializer(resp)
    assert parser.serialize(bulk, error) == expected

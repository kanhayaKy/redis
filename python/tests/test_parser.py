import pytest
from utils import RESPParser


test_cases = [
    {"resp": "$-1\r\n", "parsed": None},
    {"resp": "*1\r\n$4\r\nping\r\n", "parsed": ["ping"]},
    {
        "resp": "*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n",
        "parsed": ["echo", "hello world"],
    },
    {"resp": "*2\r\n$3\r\nget\r\n$3\r\nkey\r\n", "parsed": ["get", "key"]},
    {"resp": "+OK\r\n", "parsed": "OK"},
    {"resp": "-Error message\r\n", "parsed": "Error message"},
    {"resp": "$0\r\n\r\n", "parsed": ""},
    {"resp": "+hello world\r\n", "parsed": "hello world"},
]


def test_parser():
    for case in test_cases:
        parser = RESPParser(case.get("resp").encode())
        assert parser.parse() == case.get("parsed")

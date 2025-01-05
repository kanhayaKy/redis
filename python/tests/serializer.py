from ..serialize import serialize

test_cases = [
    {"input": "$-1\r\n", "output": None},
    {"input": "*1\r\n$4\r\nping\r\n", "output": ["ping"]},
    {
        "input": "*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n",
        "output": ["echo", "hello world"],
    },
    {"input": "*2\r\n$3\r\nget\r\n$3\r\nkey\r\n", "output": ["get", "key"]},
    {"input": "+OK\r\n", "output": "OK"},
    {"input": "-Error message\r\n", "output": "Error message"},
    {"input": "$0\r\n\r\n", "output": ""},
    {"input": "+hello world\r\n", "output": "hello world"},
]


for test in test_cases:
    print(f"Running test with {test.get('input')}")
    assert serialize(test.get("input")) == test.get("output")

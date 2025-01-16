from io import BytesIO

CRLF = b"\r\n"
CRLF_STR = "\r\n"


class RESPParser:
    def __init__(self, data: bytes, encoding: str = "utf-8"):
        self._buffer = BytesIO(data)
        self.encoding = encoding

    def _readline(self) -> bytes:
        """Reads a line ending with CRLF."""
        line = self._buffer.readline()

        # readline reads upto CRLF or LF both, A line can have LF but it always ends with CRLF
        while not line.endswith(CRLF):
            line += self._read_buffer()

        return line

    def _decode(self, data: bytes) -> str:
        """Decodes RESP data from bytes to a string."""
        return data.rstrip(CRLF).decode(self.encoding)

    def parse_simple_string(self) -> str:
        """
        Parses a RESP simple string, starting with '+'.
        Simple strings are terminated by CRLF.
        """
        line = self._buffer.readline()
        if not line.endswith(CRLF):
            raise ValueError("Not a valid simple string")

        return self._decode(line)

    def parse_bulk_string(self) -> str | None:
        """
        Parses a RESP bulk string, starting with '$'.
        Bulk strings are encoded as: $<length>\r\n<data>\r\n.
        """
        length = self.parse_integer()
        if length == -1:
            return None

        # The decode method expects the CRLF, hence reading length+2
        return self._decode(self._buffer.read(length + 2))

    def parse_integer(self) -> int:
        """
        Parses a RESP integer, starting with ':'.
        Integers are terminated by CRLF.
        """
        return int(self._decode(self._readline()))

    def parse_error(self) -> str:
        """
        Parses a RESP error message, starting with '-'.
        Errors are terminated by CRLF.
        """
        return self._decode(self._readline())

    def parse_array(self) -> list | None:
        """
        Parses a RESP array, starting with '*'.
        Arrays are encoded as: *<number of elements>\r\n<elements...>.
        """
        arr_length = self.parse_integer()

        if arr_length == -1:
            return None

        return [self.parse() for _ in range(arr_length)]

    def parse(self):
        """
        Parses the next RESP-encoded value.
        Determines the type based on the first byte.
        """
        operation_type = self._buffer.read(1)
        switcher = {
            b"+": self.parse_simple_string,
            b"-": self.parse_error,
            b":": self.parse_integer,
            b"$": self.parse_bulk_string,
            b"*": self.parse_array,
        }
        if operation_type not in switcher:
            raise ValueError(
                f"Invalid RESP data: Unknown type '{operation_type.decode(self.encoding)}'"
            )
        return switcher[operation_type]()


class RESPSerializer:
    CRLF = "\r\n"

    def __init__(self, data, encoding="utf-8"):
        self._data = data
        self.encoding = encoding

    def encode(self, data):
        """Helper method to append CRLF and encode."""
        return (data + self.CRLF).encode(self.encoding)

    def parse_bulk_string(self, data):
        """Serialize bulk string."""
        if data is None:
            return self.encode("$-1")
        return self.encode(f"${len(data)}{self.CRLF}{data}")

    def parse_string(self, data):
        """Serialize simple string."""
        return self.encode(f"+{data}")

    def parse_int(self, data):
        """Serialize integer."""
        return self.encode(f":{data}")

    def parse_error(self, data):
        """Serialize error string."""
        return self.encode(f"-{data}")

    def parse_array(self, data):
        """Serialize an array."""
        result = [self.encode(f"*{len(data)}")]
        for item in data:
            result.append(self.serialize_item(item, bulk=isinstance(item, str)))
        return b"".join(result)

    def serialize_item(self, item, bulk=False, error=False):
        """Serialize an individual item based on type or flags."""
        if error:
            return self.parse_error(item)
        if bulk:
            return self.parse_bulk_string(item)

        if isinstance(item, str):
            return self.parse_string(item)
        if isinstance(item, int):
            return self.parse_int(item)
        if isinstance(item, list):
            return self.parse_array(item)

        raise ValueError("Unsupported data format")

    def serialize(self, bulk=False, error=False):
        """Serialize the main data object."""
        return self.serialize_item(self._data, bulk, error)

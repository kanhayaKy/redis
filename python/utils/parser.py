from io import BytesIO

CRLF = b"\r\n"
CRLF_STR = "\r\n"


class RESPParser:
    def __init__(self, data, encoding="utf-8"):
        self._buffer = BytesIO(data)
        self.encoding = encoding

    def _readline(self):
        line = self._buffer.readline()

        # readline reads upto CRLF or LF both, A line can have LF but it always ends with CRLF
        while not line.endswith(CRLF):
            line += self._read_buffer()

        return line

    def _decode(self, data):
        return data.rstrip(CRLF).decode(self.encoding)

    def parse_simple_string(self):
        """
        Simple strings are encoded as a plus (+) character, followed by a string.
        The string mustn't contain a CR (\r) or LF (\n) character and is terminated by CRLF
        """
        line = self._buffer.readline()
        if not line.endswith(CRLF):
            raise "Not a valid simple string"

        return self._decode(line)

    def parse_bulk_string(self):
        """
        RESP encodes bulk strings in the following way:
        $<length>\r\n<data>\r\n

        The dollar sign ($) as the first byte.
        One or more decimal digits (0..9) as the string's length, in bytes, as an unsigned, base-10 value.
        The CRLF terminator.
        The data.
        A final CRLF.
        """

        length = self.parse_integer()

        if length == -1:
            return None

        # The decode method expects the CRLF, hence reading length+2
        return self._decode(self._buffer.read(length + 2))

    def parse_integer(self):
        return int(self._decode(self._readline()))

    def parse_error(self):
        return self._decode(self._readline())

    def parse_array(self):
        arr_length = self.parse_integer()

        if arr_length == -1:
            return None

        return [self.parse() for _ in range(arr_length)]

    def parse(self):
        operation_type = self._buffer.read(1)

        switcher = {
            b"+": self.parse_simple_string,
            b"-": self.parse_error,
            b":": self.parse_integer,
            b"$": self.parse_bulk_string,
            b"*": self.parse_array,
        }

        if operation_type not in switcher:
            raise "Invalid RESP data"

        operation = switcher[operation_type]
        return operation()

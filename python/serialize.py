def parse_simple_string(msg):
    formatted_msg = msg.replace("\r\n", "")
    return formatted_msg[1:]


def parse_error(msg):
    msg = msg.replace("\r\n", "")
    return msg[1:]


def parse_integer(msg):
    msg = msg.split("\r\n")
    return int(msg[1:])


def parse_bulk_string(msg):
    formatted_msg = msg.split("\r\n")

    if formatted_msg[0][1:] == "-1":
        return None

    return formatted_msg[1]


def parse_array(resp_msg, level=1):
    msg = resp_msg.split("\r\n")
    arr_len_str = msg[0][1:]
    arr_len = int(arr_len_str)

    current = 1

    output = []
    for _ in range(arr_len):
        first, second = msg[current], msg[current + 1]
        item = serialize(first + "\r\n" + second, level + 1)
        output.append(item)
        current += 2

    return output


def serialize(resp_msg, level=1):
    switcher = {
        "+": parse_simple_string,
        "-": parse_error,
        ":": parse_integer,
        "$": parse_bulk_string,
        "*": parse_array,
    }

    first_char = resp_msg[0]

    parser = switcher.get(first_char)

    if level > 2 and first_char == "*":
        return

    if not parser:
        return

    if parser is parse_array:
        return parser(resp_msg, level)

    return parser(resp_msg)

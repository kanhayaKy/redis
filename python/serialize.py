def parse_simple_string(msg):
    return msg[1:]


def parse_error(msg):
    return msg[1:]


def parse_integer(msg):
    return int(msg[1:])


def parse_bulk_string(msg):
    print(msg)
    formatted_msg = msg.split()
    print(formatted_msg)

    if formatted_msg[0][1:] == "-1":
        return None

    return formatted_msg[1]


def parse_array(msg):
    formatted_msg = msg.split()
    arr_len = int(formatted_msg[0][1:])

    if arr_len == -1:
        return None

    arr = []
    for i in range(arr_len):
        first, second = formatted_msg[i], formatted_msg[1]
        item = serialize(first + "\r\n" + second)
        arr.append(item)
    return arr


def serialize(resp_msg):
    formatted_msg = resp_msg.strip()

    switcher = {
        "+": parse_simple_string,
        "-": parse_error,
        ":": parse_integer,
        "$": parse_bulk_string,
        "*": parse_array,
    }

    first_char = formatted_msg[0]

    parser = switcher.get(first_char)

    if not parser:
        return

    return parser(formatted_msg)

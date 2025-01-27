from time import time


def get_expiry_time_seconds(seconds):
    return int((time() + seconds) * 1000)


def get_expiry_time_milliseconds(millseconds):
    return int((time()) * 1000 + millseconds)


def get_expiry_time_unix(unix_ts):
    return unix_ts * 1000


def get_expiry_time_unix_ms(unix_ts_ms):
    return unix_ts_ms


def get_current_ts():
    return int(time() * 1000)

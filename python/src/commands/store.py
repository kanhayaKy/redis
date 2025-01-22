from threading import Lock


class DataStore:
    _instance = None
    _instance_lock = Lock()

    def __new__(cls, *args, **kwargs):

        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)

            return cls._instance

    def __init__(self):
        self._data = {}

    def set(self, key, value):
        with self._instance_lock:
            self._data[key] = value

    def get(self, key):
        return self._data.get(key)

    def delete(self, key):
        with self._instance_lock:
            del self._data[key]

    def __contains__(self, key):
        return key in self._data


RedisStore = DataStore()

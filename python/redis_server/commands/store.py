import os
import pickle
from threading import Lock

from redis_server.utils import get_current_ts


class DataValue:
    def __init__(self, data, expiry=None):
        self.data = data
        self.expiry = expiry

    def is_expired(self):
        if not self.expiry:
            return False

        current_ts = get_current_ts()
        return current_ts > self.expiry


class DataStore:
    _instance = None
    _instance_lock = Lock()

    def __new__(cls, *args, **kwargs):

        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, load_from_disk=True, file_path=None):
        if not hasattr(self, "_data"):  # Prevent reinitialization in Singleton
            self._data = {}
            self._file_path = file_path or "db.rdb"

            if load_from_disk:
                self.load_from_disk()

    def set(self, key, value, expiry=None):
        with self._instance_lock:
            self._data[key] = DataValue(data=value, expiry=expiry)

    def get(self, key):
        if key not in self._data:
            return None

        if self._data.get(key).is_expired():
            del self._data[key]
            return None

        return self._data.get(key).data

    def delete(self, key):
        with self._instance_lock:
            if key in self._data:
                del self._data[key]

    def __contains__(self, key):
        if not key in self._data:
            return False

        if self._data[key].is_expired():
            del self._data[key]
            return False

        return True

    def get_expiry(self, key):
        if key in self._data:
            return self._data.get(key).expiry

        return None

    def load_from_disk(self):
        """
        Load data from disk during initialization. If the file does not exist,
        initialize with an empty dictionary.
        """
        if os.path.exists(self._file_path):
            try:
                with open(self._file_path, "rb") as file:
                    self._data = pickle.load(file)
                    print(f"Data loaded from {self._file_path}")
            except Exception as e:
                print(f"Failed to load data from disk: {e}")
                self._data = {}
        else:
            print(f"No existing data file found. Starting fresh.")

    def save(self, file_path=None):
        """
        Save the current state of the datastore to disk.
        """

        file_path = file_path or self._file_path
        try:
            with open(file_path, "wb") as file:
                pickle.dump(self._data, file)
                print(f"Data saved to {self._file_path}")
        except Exception as e:
            print(f"Failed to save data to disk: {e}")

    def reset_db(self):
        self._data = {}


RedisStore = DataStore()

import os
import pickle
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
        if not hasattr(self, "_data"):  # Prevent reinitialization in Singleton
            self._data = {}
            self._file_path = "db.rdb"
            self.load_from_disk()

    def set(self, key, value):
        with self._instance_lock:
            self._data[key] = value

    def get(self, key):
        return self._data.get(key)

    def delete(self, key):
        with self._instance_lock:
            if key in self._data:
                del self._data[key]

    def __contains__(self, key):
        return key in self._data

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

    def save(self):
        """
        Save the current state of the datastore to disk.
        """
        try:
            with open(self._file_path, "wb") as file:
                pickle.dump(self._data, file)
                print(f"Data saved to {self._file_path}")
        except Exception as e:
            print(f"Failed to save data to disk: {e}")


RedisStore = DataStore()

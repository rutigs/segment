from datetime import datetime, timedelta

import collections
import threading


class LruCache:
    def __init__(self, capacity=64, expiry_time=3600):
        self._capacity = capacity
        self._expiry_time = expiry_time
        self._cache = collections.OrderedDict()
        self._expiry_map = {}
        self._lock = threading.Lock()


    def get(self, key):
        with self._lock:
            try:
                value = self._cache.pop(key)
                expiry_time = self._expiry_map[key]
                if expiry_time < datetime.now():
                    self._expiry_map.pop(key)
                    return None

                self._cache[key] = value
                return value
            except KeyError:
                return None

    
    def set(self, key, value):
        with self._lock:
            try:
                self._cache.pop(key)
            except KeyError:
                if len(self._cache) >= self._capacity:
                    self._cache.popitem(last=False)
            self._cache[key] = value
            self._expiry_map[key] = datetime.now() + timedelta(seconds=self._expiry_time)
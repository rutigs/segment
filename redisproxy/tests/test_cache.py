from django.test import TestCase

from ..cache import LruCache

import time


class LruCacheTestCases(TestCase):


    def test_get_set(self):
        """
        Testing get/set operations
        """
        cache = LruCache(1, 60)

        # No keys in cache yet, should be none
        self.assertEqual(cache.get("key"), None)

        # basic get
        cache.set("key", "val")
        self.assertEqual(cache.get("key"), "val")
        
        # key overwrite val
        cache.set("key", "val2")
        self.assertEqual(cache.get("key"), "val2")

        # LRU pops old key
        cache.set("key2", "val2")
        self.assertEqual(cache.get("key"), None)
        self.assertEqual(cache.get("key2"), "val2")

        # LRU pops older item part 2
        cache = LruCache(2, 60)
        cache.set("key", "val")
        cache.set("key2", "val2")
        cache.set("key3", "val3")
        self.assertEqual(cache.get("key"), None)

        _ = cache.get("key2")
        cache.set("key4", "val4")
        self.assertEqual(cache.get("key3"), None)


    def test_expiry_time(self):
        """
        test the expiry of cache items
        """
        cache = LruCache(1, 2)
        cache.set("key", "val")
        self.assertEqual(cache.get("key"), "val")
        time.sleep(2)
        self.assertEqual(cache.get("key"), None)
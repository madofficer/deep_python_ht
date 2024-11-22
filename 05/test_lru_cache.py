import unittest
from email.utils import decode_rfc2231
from functools import lru_cache, cache
from lru_cache import DLLNode, LRUCache


class TestLRUCache(unittest.TestCase):
    def setUp(self):
        self.cache = LRUCache(2)

    def test_init(self):
        self.assertEqual(self.cache._capacity, 2)
        self.assertEqual(self.cache._cache, {})

    def test_set_get(self):
        self.cache.set(1, 1)
        res = self.cache.get(1)
        self.assertEqual(res, 1)

        self.cache.set((1, 2, 3), 2)
        res = self.cache.get((1, 2, 3))
        self.assertEqual(res, 2)

        res = self.cache.get(100)
        self.assertEqual(res, None)

    def test_set_existing_key(self):
        self.cache.set(1, 100)
        res = self.cache.get(1)
        self.assertEqual(res, 100)

        self.cache.set((1, 2, 3), 77)
        res = self.cache.get((1, 2, 3))
        self.assertEqual(res, 77)

    def test_eviction(self):
        self.cache.set(1, 1)
        self.cache.set("2", "val2")
        self.cache.set(3.0, {3})
        res1 = self.cache.get(1)
        res2 = self.cache.get("2")
        res3 = self.cache.get(3.0)
        self.assertEqual(res1, None)
        self.assertEqual(res2, "val2")
        self.assertEqual(res3, {3})

    def test_eviction_order(self):
        self.cache.set(1, 10)
        self.cache.set(2, 22)
        res1 = self.cache.get(1)
        self.assertEqual(res1, 10)
        self.cache.set("3", "_3_")
        res2 = self.cache.get(2)
        self.assertEqual(res2, None)
        res3 = self.cache.get("3")
        self.assertEqual(res3, "_3_")
        res4 = self.cache.get(1)
        self.assertEqual(res4, 10)

    def test_invalid_key(self):
        self.cache.set(1, 11)
        self.cache.set(5, "55")

        with self.assertRaises(TypeError):
            self.cache.set([1], 123)
        with self.assertRaises(TypeError):
            self.cache.set({33}, 321)

        res1 = self.cache.get(1)
        res2 = self.cache.get(5)
        self.assertEqual(res1, 11)
        self.assertEqual(res2, "55")

    def test_big_cache(self):
        big_cache = LRUCache(60)

        for key in range(60):
            big_cache.set(f"{key=}", key)

        for key in range(40, 100):
            big_cache.set(f"{key=}", key)

        res1 = big_cache.get("key=0")
        self.assertEqual(res1, None)
        res2 = big_cache.get("key=39")
        self.assertEqual(res2, None)
        res3 = big_cache.get("key=40")
        self.assertEqual(res3, 40)
        big_cache.set("new_key", 41)
        res4 = big_cache.get("key=41")
        self.assertEqual(res4, None)
        res5 = big_cache.get("key=40")
        self.assertEqual(res5, 40)

    def test_non_pos_init(self):
        non_pos_obj = LRUCache(0)
        non_pos_obj.set(1, 1)
        res1 = non_pos_obj.get(1)
        self.assertEqual(res1, None)

        non_pos_obj = LRUCache(None)
        non_pos_obj.set(None, None)
        res2 = non_pos_obj.get(None)
        self.assertEqual(res2, None)

    def test_task(self):
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")

        res1 = self.cache.get("k3")
        self.assertEqual(res1, None)
        res2 = self.cache.get("k2")
        self.assertEqual(res2, "val2")
        res3 = self.cache.get("k1")
        self.assertEqual(res3, "val1")

        self.cache.set("k3", "val3")

        res4 = self.cache.get("k3")
        self.assertEqual(res4, "val3")
        res5 = self.cache.get("k2")
        self.assertEqual(res5, None)
        res6 = self.cache.get("k1")
        self.assertEqual(res6, "val1")

    def test_cap_one(self):
        obj = LRUCache(1)

        obj.set(1, 1)
        res1 = obj.get(1)
        self.assertEqual(res1, 1)
        obj.set(2, 2)
        res2 = obj.get(2)
        self.assertEqual(res2, 2)
        res3 = obj.get(1)
        self.assertEqual(res3, None)

    def test_change_existing_val(self):
        self.cache.set(1, 10)
        self.cache.set("key2", "lol")

        res1 = self.cache.get(1)
        self.assertEqual(res1, 10)
        res2 = self.cache.get("key2")
        self.assertEqual(res2, "lol")

        self.cache.set("key2", "new_str")
        res3 = self.cache.get("key2")
        self.assertEqual(res3, "new_str")
        self.cache.set(1, 111)
        res4 = self.cache.get(1)
        self.assertEqual(res4, 111)

        self.cache.set((3,), [3, 1])
        res5 = self.cache.get((3,))
        self.assertEqual(res5, [3, 1])
        res6 = self.cache.get(2)
        self.assertEqual(res6, None)

    def test_change_val_consequence(self):
        self.cache.set(1, 111)
        self.cache.set(2, 222)

        res1 = self.cache.get(1)
        self.assertEqual(res1, 111)
        res2 = self.cache.get(2)
        self.assertEqual(res2, 222)

        self.cache.set(1, 777)
        self.cache.set(7, 17)

        res3 = self.cache.get(2)
        self.assertEqual(res3, None)
        res4 = self.cache.get(1)
        self.assertEqual(res4, 777)
        res5 = self.cache.get(7)
        self.assertEqual(res5, 17)

if __name__ == "__main__":
    unittest.main()
